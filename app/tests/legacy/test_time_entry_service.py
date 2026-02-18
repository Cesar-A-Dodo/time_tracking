from app.database.session import SessionLocal
from app.models.employee import Employee
from app.models.activity import Activity
from app.services.time_entry_service import start_time_entry, finish_time_entry, TimeEntryAlreadyOpenError, TimeEntryAlreadyFinishedError
from sqlalchemy.exc import SQLAlchemyError

def run_test():
    db = SessionLocal()

    try:
        print("----- Inicio do teste service -----")

        employee = Employee(
            name="João Luz",
            role="Técnico",
            is_active=True,
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)

        activity = Activity(
            name="Instalação De Painel",
            client="Empresa B",
            estimated_time_minutes=90,
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)

        print(f"Funcionário {employee.name}, atividade {activity.name}, CRIADOS.")

        time_entry = start_time_entry(
            db=db,
            employee_id=employee.id,
            activity_id=activity.id,
        )

        print(f"Apontamento iniciado. ID: {time_entry.id}")

        try:
            start_time_entry(
                db=db,
                employee_id=employee.id,
                activity_id=activity.id,
            )
        except TimeEntryAlreadyOpenError as e:
            print("Erro esperado capturado:", e)

        finished_entry = finish_time_entry(db, time_entry.id)
        print("Apontamento finalizado com sucesso.")

        try:
            finish_time_entry(db, time_entry.id)
        except TimeEntryAlreadyFinishedError as e:
            print("Erro esperado capturado:", e)

        print("----- Teste finalizado com sucesso -----")

    except SQLAlchemyError as e:
        print("Erro de banco:", e)

    except Exception as e:
        print("Erro inesperado:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_test()
