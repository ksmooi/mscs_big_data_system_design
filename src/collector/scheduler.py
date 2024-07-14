from apscheduler.schedulers.blocking import BlockingScheduler
from data_collector import collect_and_publish_stock_data

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_and_publish_stock_data, 'interval', seconds=60)
    print("Starting scheduler")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    main()
