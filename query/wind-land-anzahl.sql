-- Anzahl aller Windeinheiten an Land, die aktuell in Betrieb sind.
select
  count(EinheitMastrNummer)
from
  EinheitWind
where
  EinheitBetriebsstatus = 35
  and EinheitSystemstatus = 472
  and Lage = (
    select
      Id
    from
      Katalogwert k
    where
      k.Wert = "Windkraft an Land"
  )
