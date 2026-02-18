class TimeEntryError(Exception):
    pass


class EmployeeInactiveError(TimeEntryError):
    pass


class OpenTimeEntryExistsError(TimeEntryError):
    pass


class InvalidStatusTransitionError(TimeEntryError):
    pass


class TimeEntryAlreadyFinalizedError(TimeEntryError):
    pass
