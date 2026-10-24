"""
seed_data.py
------------
Populates the plants table with starter info for your 6 classes.

IMPORTANT: This content is a general-knowledge starting point for your
demo UI, written from commonly known Ayurvedic/herbal and botanical
references — it is NOT verified against a peer-reviewed pharmacological
or botanical source. Before your final submission, cross-check each entry
(especially the "references" field, which currently names reference WORKS
by type/title rather than full verified citations) against real sources
and cite them properly in your report. Do not present this as an
independently verified dataset as-is.

IMPORTANT — schema change: this version adds habitat, geographical_distribution,
and references columns to the Plant model. If you already ran an earlier
version of seed_data.py, delete the old database file first so the new
columns are created:
    del plant_recognition.db      (Windows)
    rm plant_recognition.db       (Mac/Linux)
Then run this script again.

Run:
    python seed_data.py
"""

from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)

PLANTS = [
    {
        "class_label": "Ashwagandha",
        "common_name": "Ashwagandha",
        "scientific_name": "Withania somnifera",
        "family": "Solanaceae",
        "medicinal_uses": "Traditionally used as an adaptogen to reduce stress, "
                           "support energy levels, and promote general vitality.",
        "preparation_methods": "Root powder taken with warm milk or water; also "
                                "available as capsules/extracts.",
        "diseases_treated": "Stress, anxiety, fatigue, insomnia (traditional use).",
        "active_compounds": "Withanolides (steroidal lactones), alkaloids, saponins.",
        "side_effects": "May cause mild stomach upset or drowsiness in some individuals.",
        "precautions": "Avoid during pregnancy; consult a doctor if on thyroid "
                        "medication or sedatives.",
        "habitat": "Grows in dry, well-drained soils; tolerates semi-arid and "
                    "subtropical climates.",
        "geographical_distribution": "Native to India, the Middle East, and parts "
                                      "of Africa; widely cultivated across the "
                                      "Indian subcontinent.",
        "references": "Ayurvedic Pharmacopoeia of India; Indian Materia Medica "
                       "(Nadkarni); general Ayurvedic herbal literature.",
    },
    {
        "class_label": "Brahmi",
        "common_name": "Brahmi",
        "scientific_name": "Bacopa monnieri",
        "family": "Plantaginaceae",
        "medicinal_uses": "Traditionally used to support memory and cognitive function.",
        "preparation_methods": "Leaf extract, powder, or fresh leaf juice.",
        "diseases_treated": "Memory impairment, anxiety (traditional/Ayurvedic use).",
        "active_compounds": "Bacosides A and B (triterpenoid saponins).",
        "side_effects": "May cause mild digestive discomfort.",
        "precautions": "Consult a doctor before use if pregnant, breastfeeding, "
                        "or on other medications.",
        "habitat": "A wetland/marshy plant, grows in shallow water and muddy soil "
                    "near ponds and streams.",
        "geographical_distribution": "Found throughout India, and across other "
                                      "tropical and subtropical wetland regions "
                                      "of Asia.",
        "references": "Ayurvedic Pharmacopoeia of India; Indian Materia Medica "
                       "(Nadkarni); general Ayurvedic herbal literature.",
    },
    {
        "class_label": "Chamomile",
        "common_name": "Chamomile",
        "scientific_name": "Matricaria chamomilla",
        "family": "Asteraceae",
        "medicinal_uses": "Widely used as a mild sedative and digestive aid, "
                           "commonly consumed as tea.",
        "preparation_methods": "Dried flowers steeped as tea; also used in "
                                "topical preparations.",
        "diseases_treated": "Mild anxiety, insomnia, indigestion (traditional use).",
        "active_compounds": "Apigenin, chamazulene, bisabolol.",
        "side_effects": "Allergic reactions possible, especially in people "
                         "allergic to ragweed/daisies.",
        "precautions": "Avoid if allergic to plants in the Asteraceae family.",
        "habitat": "Grows in open, sunny fields and disturbed ground; prefers "
                    "temperate climates.",
        "geographical_distribution": "Native to Europe and Western Asia; now "
                                      "cultivated worldwide including in parts "
                                      "of India.",
        "references": "European Medicines Agency herbal monograph on Matricaria "
                       "chamomilla; general herbal pharmacology literature.",
    },
    {
        "class_label": "Nirgundi",
        "common_name": "Nirgundi",
        "scientific_name": "Vitex negundo",
        "family": "Lamiaceae",
        "medicinal_uses": "Traditionally used for its anti-inflammatory and "
                           "analgesic properties.",
        "preparation_methods": "Leaf paste applied topically; leaf decoction "
                                "taken orally in traditional practice.",
        "diseases_treated": "Joint pain, inflammation, headaches (traditional use).",
        "active_compounds": "Flavonoids, iridoid glycosides, essential oils.",
        "side_effects": "Limited data; generally used topically in traditional practice.",
        "precautions": "Consult a healthcare provider before internal use.",
        "habitat": "A hardy shrub found along riverbanks, wastelands, and "
                    "roadside scrub.",
        "geographical_distribution": "Native to South and Southeast Asia; common "
                                      "throughout the Indian subcontinent.",
        "references": "Ayurvedic Pharmacopoeia of India; Indian Materia Medica "
                       "(Nadkarni); general Ayurvedic herbal literature.",
    },
    {
        "class_label": "Purna nava",
        "common_name": "Punarnava",
        "scientific_name": "Boerhavia diffusa",
        "family": "Nyctaginaceae",
        "medicinal_uses": "Traditionally used as a diuretic and for supporting "
                           "kidney/liver function.",
        "preparation_methods": "Root powder or decoction.",
        "diseases_treated": "Edema, urinary issues (traditional/Ayurvedic use).",
        "active_compounds": "Punarnavine, boeravinones, flavonoids.",
        "side_effects": "May interact with diuretic medications.",
        "precautions": "Avoid during pregnancy; consult a doctor if on "
                        "blood pressure or diuretic medication.",
        "habitat": "A common weed of fields, wastelands, and roadsides; thrives "
                    "in disturbed, sandy soils.",
        "geographical_distribution": "Widely distributed across India and other "
                                      "tropical regions of Asia, Africa, and the "
                                      "Americas.",
        "references": "Ayurvedic Pharmacopoeia of India; Indian Materia Medica "
                       "(Nadkarni); general Ayurvedic herbal literature.",
    },
    {
        "class_label": "Vasaka",
        "common_name": "Vasaka",
        "scientific_name": "Justicia adhatoda",
        "family": "Acanthaceae",
        "medicinal_uses": "Traditionally used as a respiratory remedy, "
                           "particularly for cough and bronchitis.",
        "preparation_methods": "Leaf decoction or syrup.",
        "diseases_treated": "Cough, bronchitis, asthma (traditional use).",
        "active_compounds": "Vasicine, vasicinone (quinazoline alkaloids).",
        "side_effects": "Generally well tolerated in traditional dosages.",
        "precautions": "Avoid high doses during pregnancy.",
        "habitat": "Grows as a shrub in hedges, wastelands, and along field "
                    "borders; prefers moist, well-drained soil.",
        "geographical_distribution": "Native to South Asia; common throughout "
                                      "the Indian subcontinent.",
        "references": "Ayurvedic Pharmacopoeia of India; Indian Materia Medica "
                       "(Nadkarni); general Ayurvedic herbal literature.",
    },
]


def seed():
    db = SessionLocal()
    try:
        for plant_data in PLANTS:
            existing = db.query(models.Plant).filter(
                models.Plant.class_label == plant_data["class_label"]
            ).first()
            if existing:
                # Update existing record in place so re-running this script
                # after adding new fields refreshes old rows too.
                for key, value in plant_data.items():
                    setattr(existing, key, value)
                print(f"Updated {plant_data['class_label']}")
                continue
            plant = models.Plant(**plant_data)
            db.add(plant)
            print(f"Added {plant_data['class_label']}")
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("\nSeeding complete.")
