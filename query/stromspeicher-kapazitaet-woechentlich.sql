-- Neue Bruttoleistung pro Kalenderwoche aller Photovoltaikeinheiten seit Beginn 2022.
with AnlageMitAnzahl as (
  select
    a.MaStRNummer,
    a.NutzbareSpeicherkapazitaet,
    (
      select
        count(*)
      from
        EinheitStromSpeicher e
      where
        e.SpeMastrNummer = a.MaStRNummer
    ) as AnzahlEinheiten
  from
    AnlageStromSpeicher a
),
EinheitMitKapazitaet as (
  select
    strftime("%Y-%W", Inbetriebnahmedatum) as Kalenderwoche,
    NutzbareSpeicherkapazitaet / AnzahlEinheiten as EinheitKapazitaet
  from
    EinheitStromSpeicher e
    join AnlageMitAnzahl a on e.SpeMastrNummer = a.MaStRNummer
  where
    Inbetriebnahmedatum >= "2022-01-01"
),
ProWoche as (
  select
    Kalenderwoche,
    sum(EinheitKapazitaet) as KapazitaetKumulativ
  from
    EinheitMitKapazitaet
  group by
    Kalenderwoche
)
select
  json_group_object(
    Kalenderwoche,
    round(KapazitaetKumulativ, 3)
  )
from
  ProWoche
