import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bankingsys.models import User, Test, Client, ExchangeRate, Account, JudicialHold, AccountMovement


def create_data():
    print("Cargando datos de prueba...")

    # Limpiar datos existentes primero
    print("Limpiando datos existentes...")
    User.objects.all().delete()
    Test.objects.all().delete()
    Client.objects.all().delete()
    ExchangeRate.objects.all().delete()
    Account.objects.all().delete()
    JudicialHold.objects.all().delete()
    AccountMovement.objects.all().delete()

    # === Users ===
    try:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@bank.com',
            password='admin',
            first_name='Carlos',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        print("✅ Usuario admin creado")
    except Exception as e:
        print(f"❌ Error creando admin: {e}")
        return

    try:
        empleado_user = User.objects.create_user(
            username='empleado',
            email='empleado@bank.com',
            password='empleado',
            first_name='Ana',
            last_name='Empleado',
            is_staff=True,
            is_superuser=False,
            is_active=True
        )
        print("✅ Usuario empleado creado")
    except Exception as e:
        print(f"❌ Error creando empleado: {e}")
        return

    # === Tests ===
    test1 = Test.objects.create(name='Carga inicial')
    test2 = Test.objects.create(name='Prueba movimientos')
    print("✅ Tests creados")

    # === Clients ===
    client1 = Client.objects.create(
        code='C001',
        client_type='natural',
        dni='12345678',
        name='Juan Pérez',
        address='Av. Siempre Viva 123',
        phone='987654321',
        email='juan.perez@mail.com'
    )

    client2 = Client.objects.create(
        code='C002',
        client_type='legal',
        ruc='20123456789',
        name='Inversiones SAC',
        address='Calle Falsa 456',
        phone='912345678',
        email='contacto@inversiones.com'
    )
    print("✅ Clientes creados")

    # === Exchange Rates ===
    exchange_rate = ExchangeRate.objects.create(
        date=timezone.now().date(),
        rate=3.8500
    )
    print("✅ Tasas de cambio creadas")

    # === Accounts ===
    account1 = Account.objects.create(
        client=client1,
        account_number='191-00000001-0-01',
        account_type='savings',
        currency='PEN',
        balance=1500.00,
        status='active',
        overdraft_limit=0.00
    )

    account2 = Account.objects.create(
        client=client1,
        account_number='191-00000002-0-02',
        account_type='current',
        currency='USD',
        balance=500.00,
        status='active',
        overdraft_limit=1000.00
    )

    account3 = Account.objects.create(
        client=client2,
        account_number='191-00000003-0-03',
        account_type='term',
        currency='PEN',
        balance=10000.00,
        status='active',
        overdraft_limit=0.00,
        term_months=12,
        monthly_interest=2.50
    )
    print("✅ Cuentas creadas")

    # === Judicial Holds === (OMITIDO POR ERROR EN EL MODELO)
    print("⏭️  Retenciones judiciales omitidas (error en modelo)")

    # === Account Movements ===
    movement1 = AccountMovement.objects.create(
        account=account1,
        movement_type='deposit',
        amount=500.00,
        currency='PEN',
        description='Depósito en ventanilla',
        origin_of_funds='Sueldo'
    )

    movement2 = AccountMovement.objects.create(
        account=account1,
        movement_type='withdrawal',
        amount=200.00,
        currency='PEN',
        description='Retiro en cajero'
    )

    movement3 = AccountMovement.objects.create(
        account=account1,
        movement_type='transfer',
        amount=100.00,
        currency='PEN',
        description='Transferencia a cuenta corriente',
        related_account=account2
    )

    movement4 = AccountMovement.objects.create(
        account=account2,
        movement_type='deposit',
        amount=100.00,
        currency='USD',
        description='Transferencia recibida desde ahorros',
        related_account=account1
    )

    movement5 = AccountMovement.objects.create(
        account=account3,
        movement_type='cancellation',
        amount=10000.00,
        currency='PEN',
        description='Cancelación anticipada'
    )
    print("✅ Movimientos de cuenta creados")

    print("🎉 DATOS CARGADOS EXITOSAMENTE!")
    print("\n📊 Resumen:")
    print("   - 2 usuarios creados (admin/admin, empleado/empleado)")
    print("   - 2 clientes creados")
    print("   - 3 cuentas bancarias")
    print("   - 5 movimientos de cuenta")
    print("   - Retenciones judiciales omitidas (error en modelo)")
    print("\n🔑 Usuarios para acceder:")
    print("   - Administrador: admin / admin")
    print("   - Empleado: empleado / empleado")


if __name__ == '__main__':
    create_data()