import numpy as np
import pandas as pd
from utils.log import print_log 


def mount_data(meter: pd.DataFrame, par: dict) -> np.ndarray:
    """ 
    Reads data from dataframe generator and resamples it to 6s.
    In case active power cannot be mounted, it warns user and mounts apparent power. 
    """ 
    # Load power meter data.
    df = next(meter.load(physical_quantity='power'))
    
    # Resample power data to "6s" and in case data is missing, back fill 10 samples
    df = df.resample(''f'{par["resample_period"]}s').ffill(limit=par["fill_limit"])

    # Implementation with no backfill, resamples power data to "6s", works only when sample rate of source data set it 6s.
    #df = df.resample("6s").asfreq()

    # Get time stamps. ## check why 10^9
    time_stamps = df.index.view(np.int64)//10**9

    # Try mount active power, if unsuccessful use apparent.
    try:
        ts = df.power.active.values.transpose()
    except:
        print_log(par,"no active power!")
        try:
            print_log(par,"using apparent power!")
            ts = df.power.apparent.values.transpose()
        except:
            print_log(par,"no apparent power!")
            raise ValueError
    
    return [ts, time_stamps]


def append_images(state: np.ndarray, state_stack: np.ndarray, state_stack_tmp: np.ndarray, sig: np.ndarray, sig_stack: np.ndarray, sig_stack_tmp: np.ndarray, timestamp_stack: np.ndarray, timestamp_stack_tmp: np.ndarray, time_stamp: np.ndarray, last_stamp: int, par: dict):
    """
    Appends images and ts to main array.
    In case of video, it first appends N images to temporary array, and then to main array.   

    :param img: Current image.
    :param state_stack: Array of all images.
    :param state_stack_tmp: Array of N temporary images.

    :param sig: Current power signal.
    :param sig_stack: Array of all signals. 
    :param sig_stack_tmp: Array of N temporary signals.

    :param time_stamp: Array of time stamps
    :param last_stamp: Value of last time stamp, from previous iteration.
    :param par: Dictionary of user defined parameters.

    :return: Appended state_stack and sig_stack. 
    :return last_stamp: Updated with new last time stamp.
    """

    delta = time_stamp[0] - last_stamp
    last_stamp = time_stamp[-1]

    if delta <= par["allowed_delta_between_frames"] or sig_stack_tmp.shape[0] == 0: 
        
        # Add new axis for compatibility.
        time_stamp = time_stamp[np.newaxis,...]
        sig = sig[np.newaxis,:] 

        # Append only if images are strictly in series.
        sig_stack_tmp = np.append(sig_stack_tmp, sig, axis=0)
        timestamp_stack_tmp = np.append(timestamp_stack_tmp, time_stamp, axis=0)
        state_stack_tmp = np.append(state_stack_tmp, state)

        if state_stack_tmp.shape[0] == par["frames"]:
            
            # Append signal data to main array.
            sig_stack_tmp = sig_stack_tmp[np.newaxis, ...]
            sig_stack = np.append(sig_stack, sig_stack_tmp, axis=0)

            # Add timestamp to an array
            timestamp_stack_tmp = timestamp_stack_tmp[np.newaxis, ...]
            timestamp_stack = np.append(timestamp_stack, timestamp_stack_tmp, axis=0)
            
            # Append state to main array.
            state_stack_tmp = state_stack_tmp[np.newaxis, ...]
            state_stack = np.append(state_stack, state_stack_tmp, axis=0)

            # Reset stack
            timestamp_stack_tmp = np.zeros([0, par["ts_size"]])
            sig_stack_tmp = np.zeros([0, par["ts_size"]])
            state_stack_tmp = np.zeros([0, par["img_size"], par["img_size"]])

    else:
        # If not in series, reset stack.
        timestamp_stack_tmp = np.zeros([0, par["ts_size"]])
        sig_stack_tmp = np.zeros([0, par["ts_size"]])
        state_stack_tmp = np.zeros(0)


    return state_stack, state_stack_tmp, sig_stack, sig_stack_tmp, timestamp_stack, timestamp_stack_tmp, last_stamp