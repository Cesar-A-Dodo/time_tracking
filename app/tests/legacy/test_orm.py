from datetime import datetime
from app.database.session import SessionLocal
from app.models.employee import Employee
from app.models.activity import Activity
from app.models.time_entry import TimeEntry
from app.schemas import TimeEntryStatus


def run_test():
    db = SessionLocal()

    try:
        print("----- Inicio do teste ORM -----")

        employee = Employee(
            name = "Carlos Silva",
            role = "Eletricista",
            is_active = True
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
        
        print(f"Funcionário {employee.name},ID {employee.id} CRIADO")

        activity = Activity(
            name = "Montagem de Painel",
            client = "Empresa A",
            estimated_time_minutes = 120
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)

        print(f"Atividade de {activity.name}, ID {activity.id}, CRIADA")

        time_entry = TimeEntry(
            employee_id = employee.id,
            activity_id = activity.id,
            status = TimeEntryStatus.CRIADO,
            start_time = datetime.now()
        )
        db.add(time_entry)
        db.commit()
        db.refresh(time_entry)

        print(f"Apontamento no status {time_entry.status}, ID {time_entry.id}")

        entry_from_db = db.query(TimeEntry).first()

        print("----- Testando relacionamentos -----")
        print(f"Funcionário vinculado: {entry_from_db.employee.name}")
        print(f"Atividade vinculada: {entry_from_db.activity.name}")
        print(f"Status salvo: {entry_from_db.status}")
        print("----- Teste finalizado com sucesso -----")

    except Exception as e:
        print("Erro durante o teste:", e)
    
    finally:
        db.close()

if __name__ == "__main__":
    run_test()
