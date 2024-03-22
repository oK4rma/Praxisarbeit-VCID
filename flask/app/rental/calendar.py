import calendar

# Definiert eine Klasse für einen Mietkalender, der den Python-Standardkalender nutzt.
class rentalCalendar:
    def __init__(self):
        # Initialisiert einen Kalender-Objekt.
        self.Calendar = calendar.Calendar()

    # Gibt eine Liste der Wochen des angegebenen Monats und Jahres zurück.
    def get_days(self, month, year):
        # Jede Woche ist eine Liste von Datumsobjekten.
        return self.Calendar.monthdatescalendar(year, month)
