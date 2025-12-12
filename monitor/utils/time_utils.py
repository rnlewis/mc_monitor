class TimeUtils:

    class DHMS:
        def __init__(self, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
            self.days = days
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds

        def to_dict(self) -> dict:
            return {
                "days": self.days,
                "hours": self.hours,
                "minutes": self.minutes,
                "seconds": self.seconds,
            }

    @staticmethod
    def ticks_to_clock(ticks: int) -> str:
        hours = ((ticks / 1000) + 6) % 24
        minutes = int((ticks % 1000) * 60 / 1000)
        return f"{int(hours):02d}:{minutes:02d}"

    @staticmethod
    def ticks_to_period(ticks: int) -> str:
        if 0 <= ticks < 1000:
            return "Sunrise"
        elif 1000 <= ticks < 6000:
            return "Morning"
        elif 6000 <= ticks < 12000:
            return "Afternoon"
        elif 12000 <= ticks < 13000:
            return "Sunset"
        elif 13000 <= ticks < 18000:
            return "Evening"
        else:
            return "Night"

    @staticmethod
    def gametime_ticks_to_dhms(gametime_ticks: int) -> DHMS:
        """
        Convert Minecraft gametime_ticks into days, hours, minutes, and seconds.

        Args:
            gametime_ticks (int): Number of ticks since world start

        Returns:
            TimeUtils.DHMS: An object containing days, hours, minutes, and seconds.
        """
        days = gametime_ticks // 24000
        remainder = gametime_ticks % 24000

        hours = remainder // 1000
        remainder %= 1000

        minutes = remainder // 16
        remainder %= 16

        seconds = int(remainder * 60 / 16)  # scale leftover ticks into seconds

        return TimeUtils.DHMS(days, hours, minutes, seconds)
