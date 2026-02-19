from app.database.session import SessionLocal
from app.models.time_entry import TimeEntry
from app.schemas import TimeEntryStatus, FinishType
from app.services.employee_service import (
    create_new_employee,
    disable_employee,
)
from app.services.activity_service import (
    create_new_activity,
    disable_activity,
)
from app.services.time_entry_service import start_time_entry
from app.services.exceptions import (
    EmployeeAlreadyInactiveError,
    ActivityAlreadyInactiveError,
    ActivityInactiveError,
)


def reset_db(db):
    db.query(TimeEntry).delete()
    db.commit()


def run_test():
    db = SessionLocal()

    try:
        print("----- Teste de Employee + Activity Services -----")

        reset_db(db)

        # Cria employee via service
        employee = create_new_employee(
            db,
            name="Carlos Mendes",
            role="Eletricista",
        )

        assert employee.is_active is True
        print("Funcionário criado via service")

        # Cria activity via service
        activity = create_new_activity(
            db,
            name="Montagem de Painel",
            client="Empresa X",
            estimated_time_minutes=180,
        )

        assert activity.is_active is True
        print("Atividade criada via service")

        # Inicia apontamento
        entry = start_time_entry(db, employee.id, activity.id)
        assert entry.status == TimeEntryStatus.INICIADO
        print("Apontamento iniciado")

        # Desativar employee
        disable_employee(db, employee.id)

        db.refresh(employee)
        assert employee.is_active is False

        updated_entry = db.get(TimeEntry, entry.id)

        assert updated_entry.status == TimeEntryStatus.FINALIZADO
        assert updated_entry.finish_type == FinishType.CANCELADO
        assert updated_entry.cancel_reason == "AUTO_CANCEL_ON_EMPLOYEE_DEACTIVATION"

        print("Disable employee cancela apontamento corretamente")

        # Desativar employee novamente - erro esperado
        try:
            disable_employee(db, employee.id)
            raise AssertionError("Esperava EmployeeAlreadyInactiveError")
        except EmployeeAlreadyInactiveError:
            print("EmployeeAlreadyInactiveError capturado corretamente")

        # Desativar activity
        disable_activity(db, activity.id)

        db.refresh(activity)
        assert activity.is_active is False
        print("Disable activity funciona")
        
        # Tentar iniciar com activity inativa - erro esperado
        employee2 = create_new_employee(db, name="Ana", role="Assistente")
        try:
            start_time_entry(db, employee2.id, activity.id)
            raise AssertionError("Esperava ActivityInactiveError")
        except ActivityInactiveError:
            print("ActivityInactiveError capturado corretamente")
        
        # Desativar activity novamente - erro esperado
        try:
            disable_activity(db, activity.id)
            raise AssertionError("Esperava ActivityAlreadyInactiveError")
        except ActivityAlreadyInactiveError:
            print("ActivityAlreadyInactiveError capturado corretamente")

        print("----- Teste finalizado com sucesso -----")

    except Exception as e:
        print("Erro inesperado:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_test()
