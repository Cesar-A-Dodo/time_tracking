from time import sleep
from datetime import datetime, timezone
from app.database.session import SessionLocal
from app.models.employee import Employee
from app.models.activity import Activity
from app.services.time_entry_service import (
    start_time_entry,
    pause_time_entry,
    resume_time_entry,
    finish_time_entry,
)
from app.services.exceptions import TimeEntryAlreadyFinalizedError


def run_test():
    db = SessionLocal()

    try:
        print("----- Início do teste Service (Modelo em Blocos) -----")

        # Criar funcionário
        employee = Employee(
            name="Carlos Mendes",
            role="Eletricista",
            is_active=True
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)

        # Criar atividade
        activity = Activity(
            name="Instalação Painel Industrial",
            client="Empresa X",
            estimated_time_minutes=180
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)

        print("Funcionário e atividade criados com sucesso.")

        # START
        time_entry = start_time_entry(db, employee.id, activity.id)
        print(f"Apontamento iniciado. ID: {time_entry.id}")
        sleep(10)

        # PAUSE
        time_entry = pause_time_entry(db, time_entry.id)
        print("Apontamento pausado.")
        sleep(5)

        # RESUME
        time_entry = resume_time_entry(db, time_entry.id)
        print("Apontamento retomado.")
        sleep(10)
        
        # FINISH
        time_entry = finish_time_entry(db, time_entry.id)
        print("Apontamento finalizado com sucesso.")

        # ERRO esperado
        try:
            finish_time_entry(db, time_entry.id)
        except TimeEntryAlreadyFinalizedError as e:
            print(f"Erro esperado capturado: {e}")

        # Cálculo total
        db.refresh(time_entry)
        total_time = time_entry.calculate_total_time()

        print(f"Tempo total calculado: {total_time}")
        print("Quantidade de blocos:", len(time_entry.blocks))

        print("----- Teste finalizado com sucesso -----")

    except Exception as e:
        print("Erro inesperado:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_test()
