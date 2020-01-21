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
    from kite_simulator import SimulationSetup
    SimulationSetup()
    Logger.info('Kite Job Simulation Setup completed at: ' + str(datetime.now()), push_to_slack=True)

if now >= market_open and now <= market_close:
    # Running in different process, since Websocket reactor cannot be restarted in same process
    # Mongo CLient should not be created before forking (creating a child process), therefore creating mini functions
    #TODO: Add a check if SimulationInit was successful or not if it was successfull, skip it.
    def simulation_init_process():
        Logger.info('Running Simulation init process')
        from kite_simulator import LiveSimulator
        LiveSimulator().sim_init()

    def simulate_market_process():
        Logger.info('Running Simulate market process')
        from kite_simulator import LiveSimulator
        simulator = LiveSimulator()
        simulator.simulate_market()
        simulator.calculate_and_store_pnl()

    init_process = Process(target=simulation_init_process)
    init_process.start()
    init_process.join(timeout=None)
    simulation_process = Process(target=simulate_market_process)
    simulation_process.start()
    simulation_process.join(timeout=None)
    Logger.info('Kite Job Simulation and PNL calculation completed at: ' + str(datetime.now()), push_to_slack=True)

Logger.info('Complete!')

Logger.info('=====================Kite Job Ended at: ' + str(datetime.now()))
