import os
import signal
import subprocess
import time
import argparse
import datetime

import cv2
import torch


def main(weight_nm, uuid, target_object):
    dt_now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"../data/{dt_now}"
    os.mkdir(output_dir)

    model = torch.hub.load(
        "./weights",
        "custom",
        source="local",
        path=f"weights/{weight_nm}",
        force_reload=True,
    )
    tgt_obj_set = set(target_object)

    count_val = 0
    while True:
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()

        if ret:
            count_val += 1
            result = model(frame)
            res_obj_set = set(result.pandas().xyxy[0]["name"])
            result.render()
            if (res_obj_set & tgt_obj_set) == tgt_obj_set:
                cv2.imwrite(
                    f"{output_dir}/result{count_val}.jpg",
                    result.ims[0],
                )
                p = subprocess.Popen(
                    "exec sudo ../bluez-ibeacon/bluez-beacon/ibeacon"
                    + f"200 {uuid} 0 0 -53",
                    shell=True,
                )
                time.sleep(10)
                os.kill(p.pid, signal.SIGTERM)
            else:
                print("not detected")

        camera.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-mn",
        "--weight_nm",
        help="Choose weight name for inference",
        default="yolov5s_additional_train_datahub_objects.pt",
    )
    parser.add_argument(
        "-ui",
        "--uuid",
        help="Choose uuid for BLE",
        default="62d6a9f1-9952-4a87-9c4e-3c9d2be9e380",
    )
    parser.add_argument(
        "-to",
        "--target_object",
        help="Choose object for detection",
        default=["suitcase", "book"],
        nargs="*",
    )

    args = parser.parse_args()
    weight_nm = args.weight_nm
    uuid = args.uuid
    target_object = args.target_object
    main(weight_nm, uuid, target_object)
