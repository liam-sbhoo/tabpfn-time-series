import logging
from enum import Enum

from autogluon.timeseries import TimeSeriesDataFrame

from tabpfn_time_series.tabpfn_worker import TabPFNClient, LocalTabPFN
from tabpfn_time_series.defaults import (
    TABPFN_TS_DEFAULT_QUANTILE_CONFIG,
    TABPFN_TS_DEFAULT_CONFIG,
)

logger = logging.getLogger(__name__)


class TabPFNMode(Enum):
    LOCAL = "tabpfn-local"
    CLIENT = "tabpfn-client"


class TabPFNTimeSeriesPredictor:
    """
    Given a TimeSeriesDataFrame (multiple time series), perform prediction on each time series individually.
    """

    def __init__(
        self,
        tabpfn_mode: TabPFNMode = TabPFNMode.CLIENT,
        config: dict = TABPFN_TS_DEFAULT_CONFIG,
    ) -> None:
        worker_mapping = {
            TabPFNMode.CLIENT: lambda: TabPFNClient(config),
            TabPFNMode.LOCAL: lambda: LocalTabPFN(config),
        }
        self.tabpfn_worker = worker_mapping[tabpfn_mode]()

    def predict(
        self,
        train_tsdf: TimeSeriesDataFrame,  # with features and target
        test_tsdf: TimeSeriesDataFrame,  # with features only
        quantile_config: list[float] = TABPFN_TS_DEFAULT_QUANTILE_CONFIG,
    ) -> TimeSeriesDataFrame:
        """
        Predict on each time series individually (local forecasting).
        """

        logger.info(
            f"Predicting {len(train_tsdf.item_ids)} time series with config{self.tabpfn_worker.config}"
        )

        return self.tabpfn_worker.predict(train_tsdf, test_tsdf, quantile_config)