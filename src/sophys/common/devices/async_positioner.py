import asyncio
import functools

from typing import Optional

import numpy as np

from ophyd_async.core import (
    AsyncStatus,
    SignalR,
    SignalW,
    StandardReadable,
    WatchableAsyncStatus,
    WatcherUpdate,
    observe_value,
    DEFAULT_TIMEOUT,
)


class BasePositioner(StandardReadable):
    """
    Base class for a positioner device in ophyd-async.

    This works similarly to the PVPositioner* devices in regular ophyd.
    """

    readback: SignalR
    setpoint: SignalW

    actuate: Optional[SignalW] = None
    actuate_value: Optional[float] = 1.0

    done: Optional[SignalR] = None
    done_value: Optional[float] = 1.0

    atol: Optional[float] = 1.0e-8
    rtol: Optional[float] = 1.0e-5

    def set_name(self, name: str, *, child_name_separator: str | None = None) -> None:
        super().set_name(name, child_name_separator=child_name_separator)

        self.readback.set_name(name)

    def _check_done_signal(self, new_done_value: float, is_done_event: asyncio.Event):
        if new_done_value == self.done_value:
            is_done_event.set()

    @WatchableAsyncStatus.wrap
    async def set(self, value: float, timeout=DEFAULT_TIMEOUT):
        initial_value = await self.readback.get_value()

        await self.setpoint.set(value, wait=True)

        is_done_signal_done = asyncio.Event()

        if self.actuate is not None:
            await self.actuate.set(self.actuate_value, wait=False)

        done_status = None
        if self.done is not None:
            self.done.subscribe_value(
                functools.partial(
                    self._check_done_signal, is_done_event=is_done_signal_done
                )
            )
            done_status = AsyncStatus(is_done_signal_done.wait())
        else:
            is_done_signal_done.set()

        async for current_value in observe_value(
            self.readback, done_status=done_status, done_timeout=timeout
        ):
            yield WatcherUpdate(
                current=current_value,
                initial=initial_value,
                target=value,
                name=self.name,
            )

            if (
                np.isclose(current_value, value, atol=self.atol, rtol=self.rtol)
                and is_done_signal_done.is_set()
            ):
                break
