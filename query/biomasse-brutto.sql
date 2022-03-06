-- Bruttoleistung aller Biomasseeinheiten, die aktuell in Betrieb sind.
select
  sum(Bruttoleistung)
from
  EinheitBiomasse
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
