from webscraper.index_historical import IndexHistoricalOptions
from tasks.traded_to_percent_delivered import TradedToPercentDelivered, TradedToPercentDeliveredReport
from kite_simulator import SimulationSetup, LiveSimulator
from util.log import Logger
from datetime import datetime
from dateutil.tz import *
import time
from multiprocessing import Process


Logger.info('=====================Kite Job Starting at: ' + str(datetime.now()))

now = datetime.now().astimezone(tzlocal())
market_open = now.replace(hour=9, minute=15)
market_close = now.replace(hour=15, minute=30)
market_preopen_open = now.replace(hour=9, minute=0)
market_preopen_close = market_open


if now >= market_preopen_open and now <= market_open:
    SimulationSetup()
    Logger.info('Kite Job Simulation Setup completed at: ' + str(datetime.now()), push_to_slack=False)

if now >= market_open and now <= market_close:
    # Running in different process, since Websocket reactor cannot be restarted in same process
    simulator = LiveSimulator()
    init_process = Process(target=simulator.sim_init)
    init_process.start()
    init_process.join(timeout=None)
    simulation_process = Process(target=simulator.simulate_market)
    simulation_process.start()
    simulation_process.join(timeout=None)
    simulator.calculate_and_store_pnl()
    Logger.info('Kite Job Simulation and PNL calculation completed at: ' + str(datetime.now()), push_to_slack=False)

Logger.info('Complete!')

Logger.info('=====================Kite Job Ended at: ' + str(datetime.now()))
