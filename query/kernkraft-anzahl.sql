-- Anzahl aller Kernkrafteinheiten, die aktuell in Betrieb sind.
select
  count(EinheitMastrNummer)
from
  EinheitKernkraft
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
