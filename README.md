# UrbanSolar Battery - Personal Test Fork

![HACS Integration](https://img.shields.io/badge/HACS-Integration-blue?logo=home-assistant)
![Home Assistant](https://img.shields.io/badge/Compatible-Home%20Assistant-41BDF5?logo=home-assistant)
![Status](https://img.shields.io/badge/Status-Personal%20test%20fork-orange)

> **Fork notice:** This is an unofficial personal test fork. It is not affiliated with or supported by the original project. It is provided "as is", without support or warranty.

---

## 📚 Sommaire

1. [Ajouter le dépôt HACS](#ajouter-le-depot-hacs)
2. [Installer l'intégration](#installer-lintegration)
3. [Configuration](#configuration)
4. [Entités & Automatisations](#entites-et-automatisations)
5. [Dashboard Lovelace](#dashboard-lovelace)
6. [Dépannage](#depannage)
7. [À propos de ce fork](#a-propos-de-ce-fork)

---

<a id="ajouter-le-depot-hacs"></a>
## 1. Ajouter le dépôt HACS

1. Ouvrez **HACS** dans Home Assistant.  
2. Allez dans l’onglet **Intégrations**.  
3. Cliquez sur **➕ Ajouter un dépôt personnalisé** et entrez l’URL :  
  `https://github.com/BeletteHome/ha-urbansolar-bv`
4. Sélectionnez **Catégorie : Intégration**.  
5. Cliquez sur **Enregistrer**

---

<a id="installer-lintegration"></a>
## 2. Installer l'intégration

1. Dans **HACS → Intégrations**, recherchez **UrbanSolar Battery**.  
2. Cliquez sur **Télécharger**.  
3. **Redémarrez Home Assistant**.

### 📦 Dépendances Lovelace requises

L’intégration utilise plusieurs cartes Lovelace que vous devez installer via HACS :

| Carte Lovelace              | Dépôt GitHub                                                   |
|----------------------------|----------------------------------------------------------------|
| ApexCharts Card            | [apexcharts-card](https://github.com/RomRider/apexcharts-card) |
| Vertical Stack In Card     | [vertical-stack-in-card](https://github.com/custom-cards/vertical-stack-in-card) |
| Number Box Card            | [numberbox-card](https://github.com/junkfix/numberbox-card) | 
| Energy Flow Card Plus      | [energy-flow-card-plus](https://github.com/flixlix/energy-flow-card-plus) |
| Power Flow Card Plus       | [power-flow-card-plus](https://github.com/flixlix/power-flow-card-plus) |

> **N'oubliez pas de redémarrer Home Assistant** après installation.

---

<a id="configuration"></a>
## 3. Configuration

Lors de l’ajout de l’intégration, une boîte de dialogue vous demandera de sélectionner :

1. **Capteur de puissance totale consommée** (ex : `sensor.puissance_totale_consommee`)  
2. **Capteur de puissance solaire produite** (ex : `sensor.pv_energie_solaire`)

> ⚠️ Assurez-vous que ces capteurs renvoient une puissance en **kW**.

Si la boîte de dialogue ne s’affiche pas :  
→ **Paramètres → Intégrations → ➕ Ajouter** → **Urban Solar Battery**.

Ensuite, ajoutez dans votre `configuration.yaml` :

```yaml
#Urban solar
input_number: !include urban_input_numbers.yaml
sensor: !include urban_integrations.yaml
template: !include urban_sensors.yaml
utility_meter: !include urban_utility_meters.yaml
automation: !include urban_automations.yaml
```

Home Assistant accepts only one top-level `automation:` key. If you already include
your own automation file, do not add a second `automation:` entry. To load multiple
YAML automation files, move the YAML automations into separate files under an
`automations/` directory and use:

```yaml
automation: !include_dir_merge_list automations/
```

Place the UrbanSolar automations from `urban_automations.yaml` in that directory
alongside your own YAML automation files. UI-managed automations are stored
separately by Home Assistant and do not need to be moved.
---

→**Redémarrez Home Assistant après avoir enregistré configuration.yaml**

Enfin créer un dashboard/Tableau de bord
Nommez le Urban Solar Dashboard
et dans sa section yaml coller le code suivant

```yaml
views:
  - title: Urban
    sections:
      - type: grid
        cards:
          - type: custom:energy-flow-card-plus
            entities:
              battery:
                entity:
                  production: sensor.urban_batterie_virtuelle_entree_horaire
                  consumption: sensor.urban_batterie_virtuelle_sortie_horaire
                state_of_charge: input_number.urban_batterie_virtuelle_stock
                state_of_charge_unit: kwh
                use_metadata: false
              grid:
                entity:
                  consumption: sensor.urban_energie_importee_enedis
                use_metadata: false
              home:
                entity: sensor.urban_energie_consommee_totale
                subtract_individual: false
                use_metadata: false
                override_state: true
              solar:
                entity: sensor.urban_energie_solaire_produite
            clickable_entities: true
            display_zero_lines: true
            use_new_flow_rate_model: true
            energy_date_selection: false
            wh_decimals: 1
            kwh_decimals: 0
            min_flow_rate: 1
            max_flow_rate: 6
            max_expected_energy: 2000
            min_expected_energy: 10
            wh_kwh_threshold: 1000
            title: Energy Flow Card
          - type: custom:apexcharts-card
            graph_span: 3d
            span:
              end: minute
            header:
              show: true
              title: Batterie Virtuelle
              show_states: true
              colorize_states: true
            series:
              - entity: input_number.urban_batterie_virtuelle_stock
                yaxis_id: first
                name: Stock batterie
                type: line
                group_by:
                  duration: 0.5h
                  func: last
                stroke_width: 3
              - entity: input_number.urban_batterie_virtuelle_pointage
                yaxis_id: first
                name: Pointage manuel
                type: line
                stroke_width: 3
                color: '#995000'
                show:
                  in_chart: false
            yaxis:
              - id: first
                decimals: 1
                apex_config:
                  tickAmount: 4
          - type: custom:power-flow-card-plus
            entities:
              battery:
                entity:
                  consumption: sensor.urban_puissance_batterie_virtuelle_out
                  production: sensor.urban_puissance_batterie_virtuelle_in
                state_of_charge: input_number.urban_batterie_virtuelle_stock
                display_state: one_way_no_zero
                state_of_charge_unit: kwh
                show_state_of_charge: true
                use_metadata: true
                color_circle: true
              grid:
                entity: sensor.urban_puissance_import_enedis
                display_state: one_way
                secondary_info: {}
              solar:
                entity: sensor.urban_puissance_solaire_instant
                display_zero_state: true
                secondary_info: {}
              home:
                secondary_info: {}
                entity: sensor.urban_conso_totale_instant
                override_state: true
            clickable_entities: true
            display_zero_lines: true
            use_new_flow_rate_model: true
            w_decimals: 0
            kw_decimals: 1
            min_flow_rate: 0.75
            max_flow_rate: 6
            max_expected_power: 2000
            min_expected_power: 0.01
            watt_threshold: 1000
            transparency_zero_lines: 0
            sort_individual_devices: false
            title: Power Flow Card
          - type: custom:apexcharts-card
            graph_span: 3d
            span:
              end: minute
            header:
              show: true
              title: Bilan energie réseau
              show_states: true
              colorize_states: true
            apex_config:
              chart:
                type: line
            series:
              - entity: sensor.urban_energie_restituee_au_reseau
                yaxis_id: first
                type: line
                color: green
                group_by:
                  duration: 0.5d
                  func: diff
                name: Variation quotidienne
            yaxis:
              - id: first
                decimals: 0
                apex_config:
                  tickAmount: 4
          - type: custom:apexcharts-card
            graph_span: 3day
            span:
              end: minute
            header:
              show: true
              title: Batterie Virtuelle - Flux Horaire
              show_states: true
              colorize_states: true
            apex_config:
              chart:
                type: area
              stroke:
                curve: smooth
            series:
              - entity: input_number.urban_energie_battery_in_hourly
                yaxis_id: first
                name: Entrée Batterie (IN)
                type: line
                color: '#00C853'
                stroke_width: 3
                group_by:
                  duration: 1h
                  func: avg
              - entity: input_number.urban_energie_battery_out_hourly
                name: Sortie Batterie (OUT)
                yaxis_id: first
                type: line
                color: '#D50000'
                stroke_width: 3
                group_by:
                  duration: 1h
                  func: avg
              - entity: sensor.urban_energie_restituee_au_reseau_hourly
                name: Bilan energie
                yaxis_id: second
                type: line
                color: yellow
                stroke_width: 1
                group_by:
                  duration: 1h
                  func: avg
            yaxis:
              - id: first
                decimals: 1
                apex_config:
                  tickAmount: 4
              - id: second
                opposite: true
                decimals: 1
                apex_config:
                  tickAmount: 4
          - type: custom:vertical-stack-in-card
            cards:
              - type: custom:vertical-stack-in-card
                title: Batterie Virtuelle (kWh)
                cards:
                  - type: custom:numberbox-card
                    entity: input_number.urban_batterie_virtuelle_stock
                    name: Stock calculé
                    icon: mdi:battery
                    min: -100
                    max: 200
                    step: 0.1
                    unit: kWh
                    border: false
              - type: entities
                entities:
                  - entity: sensor.urban_energie_restituee_au_reseau_hourly
                    name: Variation horaire
                    icon: mdi:clock-in
                  - entity: sensor.urban_batterie_virtuelle_entree_horaire
                    secondary_info: none
                    name: 'Batt in pour dashboard energy '
                    icon: mdi:battery-arrow-down
                  - entity: sensor.urban_batterie_virtuelle_sortie_horaire
                    name: Batt out pour dashboard energy
                    icon: mdi:battery-arrow-up
                title: Index horaire et sensor horaire
                grid_options:
                  columns: 12
                  rows: 6
                state_color: true
        column_span: 3
      - type: grid
        cards:
          - type: heading
            heading_style: title
        column_span: 2
    cards: []
    type: sections
    max_columns: 3
    dense_section_placement: false

```




<a id="entites-et-automatisations"></a>
## 4. Entités & Automatisations

### Capteurs créés automatiquement

| Entité | Description |
|--------|-------------|
| `sensor.urban_energie_restituee_au_reseau` | Énergie solaire excédentaire envoyée au réseau |
| `sensor.urban_puissance_import_enedis` | Puissance importée du réseau en temps réel |
| `sensor.urban_energie_importee_enedis` | Intégration de la puissance importée |
| `sensor.urban_puissance_solaire_instant` | Puissance solaire instantanée |
| `sensor.urban_conso_totale_instant` | Puissance totale consommée |
| `sensor.urban_batterie_virtuelle_stock` | Stock actuel de la batterie virtuelle |
| `sensor.urban_batterie_virtuelle_entree_horaire` | Entrée horaire vers batterie virtuelle |
| `sensor.urban_batterie_virtuelle_sortie_horaire` | Sortie horaire depuis la batterie virtuelle |

### Input Numbers

- `input_number.urban_batterie_virtuelle_stock`
- `input_number.urban_energie_restituee_veille`

### Automatisations incluses

- Mise à jour quotidienne du stock de la batterie
- Calcul différentiel sur l’énergie exportée
- Mise à jour manuelle possible via Number Box

---

<a id="dashboard-lovelace"></a>
## 5. Dashboard Lovelace

Un **dashboard complet** est installé automatiquement via `urban_dashboard.yaml` :  
- Visualisation du flux d’énergie  
- Courbes de production et de consommation  
- Suivi du stock de la batterie virtuelle
- 2 capteurs ad'hoc disponibles pour configurer le dashboard **Energy** pour la partie batterie :
    `sensor.urban_batterie_virtuelle_entree_horaire`
    `sensor.urban_batterie_virtuelle_sortie_horaire`, pensez aussi a supprimer l'énergie retournée au réseau car l'énergie retourrne a la batterie ^^

![Capture d'écran de l'application](https://i.imgur.com/NBjRcze.png)

![Capture d'écran de l'application](https://i.imgur.com/KdZF5rX.png)

![Capture d'écran de l'application](https://i.imgur.com/vUdDOOh.png)
---

<a id="depannage"></a>
## 6. Dépannage

- **Capteur manquant (`sensor.urban_energie_restituee_au_reseau`) ?**  
  → Vérifiez votre configuration YAML et les logs de Home Assistant.

- **Pas de mise à jour nocturne ?**  
  → Assurez-vous que votre timezone est correcte.  

---

<a id="a-propos-de-ce-fork"></a>
## 7. À propos de ce fork

Ce dépôt est un fork personnel de test maintenu par BeletteHome. Il est fourni "as is" et aucun support n'est proposé. Il n'est pas affilié au projet d'origine.

---

Merci d’utiliser cette version de test d’**UrbanSolar Battery**.
