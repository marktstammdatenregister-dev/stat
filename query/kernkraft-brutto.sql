-- Bruttoleistung aller Kernkrafteinheiten, die aktuell in Betrieb sind.
select
  sum(Bruttoleistung)
from
  EinheitKernkraft
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
