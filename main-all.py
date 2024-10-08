import argparse
from manga109utils import Manga109Dataset

import order_estimator

four_panel_list = ["YouchienBoueigumi", "Akuhamu", "OL_Lunch", "TetsuSan"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=0.25)
    parser.add_argument("--dataset-root", type=str, default="./dataset/Manga109_released_2021_02_28")

    args = parser.parse_args()

    order_estimator.interception_ratio_threshold = args.threshold

    dataset = Manga109Dataset(manga109_root_dir=args.dataset_root)

    for book in dataset.get_book_iter():
        print(book.title)
        if book.title in four_panel_list:
            initial_cut_option = "two-page-four-panel"
        else:
            initial_cut_option = "two-page"

        for i_page, page in enumerate(book.get_page_iter()):
            print(f"Page {i_page}:")
            image = page.get_image()
            pagewidth = image.size[0]

            panels = page.get_bbs()["frame"]
            boxOrderEstimator = order_estimator.BoxOrderEstimator(
                panels,
                pagewidth=pagewidth,
                initial_cut_option=initial_cut_option)

            for i_panel, panel in enumerate(boxOrderEstimator.ordered_bbs):
                if len(panel.panels) == 1:
                    print(f"{i_panel:2d}: {panel}")
                else:
                    print(f"{i_panel:2d} Subpanels of {panel}:")
                    for subpanel in panel.panels:
                        print(f"    - {subpanel}")
