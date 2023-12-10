"""Wrapper for Piko object."""
import time

from kostalpiko.kostalpiko import Piko


class PikoHolder(Piko):  # type: ignore
    """Wrapper for Piko object."""

    last_update = 0.0
    update_running = False

    # def __init__(
    #     self,
    #     host: str | None = None,
    #     username: str = "pvserver",
    #     password: str = "pvwr",
    # ) -> None:
    #     """Create a new PIKO instance to update entities."""
    #     super().__init__(host, username, password)

    def update(self) -> None:
        """Pull values from PIKO."""
        if not self.update_running:
            if time.time() - self.last_update > 30.0:
                self.update_running = True
                self.last_update = time.time()
                super().update()
                self.update_running = False
