-- Anzahl aller Solareinheiten, die aktuell in Betrieb sind.
select
  count(EinheitMastrNummer)
from
  EinheitSolar
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
