import json
import multiprocessing
import multiprocessing.pool
import os
from pathlib import PurePath
import shutil
import time
from unittest import mock
from unittest.mock import MagicMock, patch
import csv

from tests.test_zmanager.testing_objects import PerformanceTestResults
from tests.test_zmanager.zmanager_connection import ServiceSimulatorMultiProc
from tests.test_zmanager.zmanager_setup import ZManagerSetup, ZmanagerMultiProcSetup, ZmanagerSingleThreadSetup

from digitalpy.core.main.singleton_configuration_factory import SingletonConfigurationFactory

def single_thread_zmanager_test_worker(zmanager_setup: ZManagerSetup, message_count: int, worker_count: int, service_count: int):

    zmanager_conf = SingletonConfigurationFactory.get_configuration_object("ZManagerConfiguration")
    zmanager_setup.start()
    time.sleep(4)

    print("starting operation")
    # run the client in a separate process so that the cpu usage can be monitored
    start_perf_counter = time.perf_counter()
    start_proc_time = time.process_time()
    procs: list[multiprocessing.Process] = []

    # start services that will send messages to the subject
    for n in range(service_count):
        messages = [f"{n}~context~action~format~protocol~{i}".encode() for i in range(int(message_count/service_count))]
        service_simulator = ServiceSimulatorMultiProc(zmanager_setup.get_subject_address(), zmanager_conf, [f"/messages{n}"])
        proc = multiprocessing.Process(target=service_simulator.start, args=(messages,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    zmanager_setup.stop()

    test_data = f"{time.perf_counter() - start_perf_counter},{time.process_time() - start_proc_time},{message_count},{message_count/(time.perf_counter() - start_perf_counter)},{worker_count}"

    return test_data

def save_to_csv(data: PerformanceTestResults, filename):
    with open(filename, "a") as file:
        writer = csv.writer(file)
        writer.writerow(data.split(","))

if __name__ == "__main__":
    #for _ in range(10):
    #    save_to_csv(single_thread_zmanager_test_worker(initialize_zmanager_single_thread, 2000000, 14), "single_thread_test.csv")
    worker_count = 10
    for _ in range(1):
        save_to_csv(single_thread_zmanager_test_worker(ZmanagerMultiProcSetup(workers=worker_count, worker_class="tests.test_zmanager.zmanager_test_worker.TestRoutingWorker"), 1000, worker_count, 1), "multi_proc_test_refactored.csv")
