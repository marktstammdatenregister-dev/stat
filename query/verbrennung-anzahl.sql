-- Anzahl aller Verbrennungseinheiten, die aktuell in Betrieb sind.
select
  count(EinheitMastrNummer)
from
  EinheitVerbrennung
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
