-- Bruttoleistung aller Biomasseeinheiten, die aktuell in Betrieb sind.
select
  count(EinheitMastrNummer)
from
  EinheitBiomasse
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
