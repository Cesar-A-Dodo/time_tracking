class ServiceError(Exception):
    pass


class TimeEntryError(ServiceError):
    pass


class EmployeeInactiveError(TimeEntryError):
    pass


class OpenTimeEntryExistsError(TimeEntryError):
    pass


class InvalidStatusTransitionError(TimeEntryError):
    pass


class TimeEntryAlreadyFinalizedError(TimeEntryError):
    pass


class EmployeeError(ServiceError):
    pass


class EmployeeNotFoundError(EmployeeError):
    pass


class EmployeeAlreadyInactiveError(EmployeeError):
    pass


class ActivityError(ServiceError):
    pass


class ActivityNotFoundError(ActivityError):
    pass


class ActivityInactiveError(ActivityError):
    pass


class ActivityAlreadyInactiveError(ActivityError):
    pass