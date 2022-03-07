-- Anzahl der Stromspeichereinheiten, die aktuell in Betrieb sind.
select
  count(EinheitMastrNummer)
from
  EinheitStromSpeicher
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
