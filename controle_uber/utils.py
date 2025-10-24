from datetime import datetime, date
import calendar

def iso(dstr):
    """Converte string dd/mm/aaaa ou aaaa-mm-dd para 'YYYY-MM-DD'."""
    dstr = dstr.strip()
    try:
        if "/" in dstr:
            d = datetime.strptime(dstr, "%d/%m/%Y").date()
        else:
            d = datetime.strptime(dstr, "%Y-%m-%d").date()
        return d.strftime("%Y-%m-%d")
    except Exception:
        raise ValueError("Use data no formato dd/mm/aaaa ou aaaa-mm-dd")

def br(diso):
    y, m, d = diso.split("-")
    return f"{d}/{m}/{y}"

def working_days_without_mon_wed(year, month):
    """Conta dias do mês exceto segunda (0) e quarta (2)."""
    # número de dias do mês
    last = calendar.monthrange(year, month)[1]
    days = 0
    for d in range(1, last+1):
        wd = calendar.weekday(year, month, d)
        if wd not in (0, 2):
            days += 1
    return days

def fmt_currency(x: float) -> str:
    """Formata número como 'R$ 1.234,56'."""
    s = f"R$ {x:,.2f}"
    # trocar pontos e vírgulas para formato brasileiro
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
