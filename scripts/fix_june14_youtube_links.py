"""One-off local fix: backfill source_url for the 2026-06-14 batch.

Purely local: edits the manifest in place and re-renders from already-stored
markdown bodies. No translation/connection API calls.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from podlens.publish import load_site_config, update_episode

URLS = {
    "adam-neumann-wework-flow-community": "https://youtu.be/RAHsF4A8GLM?si=yEde8Tld7lZRPiq1",
    "alexei-efros-surface-data-deep-data": "https://www.youtube.com/live/vk6lgHjjGp8?si=5F0NXJlFZ_LtNfgm",
    "arthur-brooks-reinvention-religion-happiness": "https://youtu.be/PIbk5AnJGqc?si=1JooTQb9D1a8bebZ",
    "daniel-ek-impact-happiness-self-mastery": "https://youtu.be/qiXH0y2V3_8?si=kNvfy4iW85RpmnUu",
    "brendan-foody-mercor-teaching-ai-knowledge-work": "https://youtu.be/zld39xD4sus?si=WrrsvImuMSX5fv4G",
    "garry-tan-yc-personal-ai-revolution": "https://youtu.be/bTxALvFKP8M?si=NluV8wvfo-MylOyk",
    "alison-gopnik-childhood-learning-ai-cultural-technology": "https://youtu.be/JIFdeXPB1Pg?si=N_faH9jRjDjsO-d9",
    "how-elon-thinks-algorithm-physics-makers": "https://youtu.be/CdBcZSau5iA?si=6fvU6uMUB1u-vN60",
    "ivanka-trump-authenticity-reinvention": "https://youtu.be/VhsiMd9ZFNk?si=WaRGKH5RIBF3lq5J",
    "james-dyson-5127-prototypes-invention": "https://youtu.be/Se64B8TKfjA?si=7yTNRW0n8_3-H-Lv",
    "john-mackey-whole-foods-44-years": "https://youtu.be/U8zqsiePKsg?si=tAe-6DiWmUOT_iCn",
    "lewis-spacex-7years-manufacturing-musk": "https://youtu.be/a93FT2340c0?si=VYbwPUuIeqiwX8vX",
    "diarmaid-macculloch-christianity-sex-history": "https://youtu.be/VeDKWf80Z3M?si=tgYchuRPSXpo_dEk",
    "marc-andreessen-malleable-world-founder-capitalism": "https://youtu.be/qBVe3M2g_SA?si=4nH-M9kcrb9AqiAB",
    "michael-ovitz-caa-frame-of-reference": "https://youtu.be/yhh-J0zVsik?si=nu1Qg1WdCz2dOm2h",
    "patrick-oshaughnessy-principle-life-work": "https://youtu.be/E8B-P1oGuz4?si=UnR_tDYITDaSYeVU",
    "pavel-durov-telegram-freedom-resistance": "https://youtu.be/qjPH9njnaVU?si=x9ebCbdRcCod6zJx",
    "rick-rubin-creative-act-less-is-more": "https://youtu.be/g6MEDOY7tHo?si=aZ4IIwsS_4AkE51D",
    "sarah-paine-continental-maritime-powers-geopolitics": "https://youtu.be/OS1NZLgKM2c?si=3tPDMLU6aQFHX9R1",
    "tobi-lutke-companies-as-technology-shopify-os": "https://youtu.be/ZSM2uFnJ5bs?si=PmSUanLOTp2sgprn",
}


def main() -> int:
    site = load_site_config()
    for slug, url in URLS.items():
        entry = update_episode(slug, site, source_url=url)
        print(f"{slug}: source_url -> {entry['source_url']}")
    print(f"\nDone. {len(URLS)} episodes updated, site rebuilt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
