import { FETCH_CARDS } from "./actionTypes";
import { FETCH_HORSE } from "./actionTypes";
import { FETCH_RACE } from "./actionTypes";
import { FETCH_TRAINER } from "./actionTypes";
import { FETCH_JOCKEY } from "./actionTypes";
import { FETCH_OWNER } from "./actionTypes";
import { FETCH_TRAINER_STATS } from "./actionTypes";
import { FETCH_JOCKEY_STATS } from "./actionTypes";
import { FETCH_OWNER_STATS } from "./actionTypes";
import { FETCH_PAST_PERFORMANCES } from "./actionTypes";
import { FETCH_RACE_PAST_PERFORMANCE } from "./actionTypes";
import { QUERY_RESULTS } from "./actionTypes";
import { INDEX_JOCKEYS } from "./actionTypes";
import { INDEX_TRAINERS } from "./actionTypes";
import { INDEX_TRACKS } from "./actionTypes";
import { QUERY_CARDS } from "./actionTypes";
import { FETCH_ENTRANTS } from "./actionTypes";
import { SEARCH_HORSES } from "./actionTypes";
import { FETCH_HOT_JOCKEYS } from "./actionTypes";
import { FETCH_HOT_TRAINERS } from "./actionTypes";
import { CLEAR_RESULTS } from "./actionTypes";
import { CLEAR_JOCKEY } from "./actionTypes";
import { CLEAR_TRAINER } from "./actionTypes";
import { CLEAR_OWNER } from "./actionTypes";
import { CLEAR_RACE } from "./actionTypes";
import { CLEAR_PAST_PERFORMANCES } from "./actionTypes";
import { CLEAR_CARDS } from "./actionTypes";
import { CLEAR_HORSE } from "./actionTypes";
import { CLEAR_HOT_JOCKEYS } from "./actionTypes";
import { CLEAR_HOT_TRAINERS } from "./actionTypes";
import { LIST_ENTRIES } from "./actionTypes";
import { CLEAR_ENTRANTS } from "./actionTypes";
import { FETCH_LIVE_PREDICTION } from "./actionTypes";
import { CLEAR_LIVE_PREDICTIONS } from "./actionTypes";
import { FETCH_LIVE_ODDS } from "./actionTypes";
import { CLEAR_LIVE_ODDS } from "./actionTypes";
import { FETCH_SIMULCAST_RACES } from "./actionTypes";

import backend from "../services/backend";

export const fetchCards = () => {
  return async (dispatch) => {
    const response = await backend.get(`/cards/`);
    dispatch({ type: FETCH_CARDS, payload: response.data });
  };
};

export const fetchHorse = (id) => {
  return async (dispatch) => {
    const response = await backend.get(`/horses/${id}`);
    dispatch({ type: FETCH_HORSE, payload: response.data });
  };
};

export const fetchTrainer = (id) => {
  return async (dispatch) => {
    const response = await backend.get(`/trainers/${id}`);
    dispatch({ type: FETCH_TRAINER, payload: response.data });
  };
};

export const fetchTrainerStats = (id, after = null) => {
  return async (dispatch) => {
    const response = await backend.post(`/trainers/stats/${id}`, {
      after,
    });
    dispatch({ type: FETCH_TRAINER_STATS, payload: response.data });
  };
};

export const fetchJockey = (id) => {
  return async (dispatch) => {
    const response = await backend.get(`/jockeys/${id}`);
    dispatch({ type: FETCH_JOCKEY, payload: response.data });
  };
};

export const fetchJockeyStats = (id, after = null) => {
  return async (dispatch) => {
    const response = await backend.post(`/jockeys/stats/${id}`, {
      after,
    });
    dispatch({ type: FETCH_JOCKEY_STATS, payload: response.data });
  };
};

export const fetchOwner = (id) => {
  return async (dispatch) => {
    const response = await backend.get(`/owners/${id}`);
    dispatch({ type: FETCH_OWNER, payload: response.data });
  };
};

export const fetchOwnerStats = (id, after = null) => {
  return async (dispatch) => {
    const response = await backend.post(`/owners/stats/${id}`, {
      after,
    });
    dispatch({ type: FETCH_OWNER_STATS, payload: response.data });
  };
};

export const fetchRace = (id) => {
  return async (dispatch) => {
    const response = await backend.get(`/races/${id}`);
    dispatch({ type: FETCH_RACE, payload: response.data });
  };
};

export const fetchPastPerformances = (id) => {
  return async (dispatch) => {
    const response = await backend.get(`/horses/${id}/past_performances`);
    const payload = {}
    payload[id] = response.data
    dispatch({ type: FETCH_PAST_PERFORMANCES, payload: payload });
  };
};

export const queryResults = (filter) => {
  return async (dispatch) => {
    const response = await backend.post(`/results/`, filter);
    dispatch({ type: QUERY_RESULTS, payload: response.data });
  };
};

export const queryEntrants = (filter) => {
  return async (dispatch) => {
    const response = await backend.post(`/entrants/`, filter);
    dispatch({ type: QUERY_RESULTS, payload: response.data });
  };
};

export const clearEntrants = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_ENTRANTS, payload: null });
  };
};

export const indexJockeys = () => {
  return async (dispatch) => {
    const response = await backend.get(`/jockeys/`);
    dispatch({ type: INDEX_JOCKEYS, payload: response.data });
  };
};

export const indexTrainers = () => {
  return async (dispatch) => {
    const response = await backend.get(`/trainers/`);
    dispatch({ type: INDEX_TRAINERS, payload: response.data });
  };
};

export const indexTracks = () => {
  return async (dispatch) => {
    const response = await backend.get(`/tracks/`);
    dispatch({ type: INDEX_TRACKS, payload: response.data });
  };
};

export const queryCards = (filter) => {
  return async (dispatch) => {
    const response = await backend.post(`/races/`, filter);
    dispatch({ type: QUERY_CARDS, payload: response.data });
  };
};

export const fetchEntrants = () => {
  return async (dispatch) => {
    const response = await backend.get(`/entrants`);
    dispatch({ type: FETCH_ENTRANTS, payload: response.data });
  };
};

export const searchHorses = (term) => {
  return async (dispatch) => {
    const response = await backend.post(`/horses/search`, { term });
    dispatch({ type: SEARCH_HORSES, payload: response.data });
  };
};

export const fetchHotJockeys = (after = null) => {
  return async (dispatch) => {
    const response = await backend.post(`/jockeys/top`, { after });
    dispatch({ type: FETCH_HOT_JOCKEYS, payload: response.data });
  };
};

export const fetchHotTrainers = (after = null) => {
  return async (dispatch) => {
    const response = await backend.post(`/trainers/top`, { after });
    dispatch({ type: FETCH_HOT_TRAINERS, payload: response.data });
  };
};

export const clearResults = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_RESULTS, payload: null });
  };
};

export const clearJockey = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_JOCKEY, payload: null });
  };
};

export const clearTrainer = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_TRAINER, payload: null });
  };
};

export const clearOwner = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_OWNER, payload: null });
  };
};

export const clearRace = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_RACE, payload: null });
  };
};

export const clearPastPerformances = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_PAST_PERFORMANCES, payload: null });
  };
};

export const clearCards = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_CARDS, payload: null });
  };
};

export const clearHorse = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_HORSE, payload: null });
  };
};

export const clearHotJockeys = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_HOT_JOCKEYS, payload: null });
  };
};

export const clearHotTrainers = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_HOT_TRAINERS, payload: null });
  };
};

export const listEntries = (data) => {
  return async (dispatch) => {
    const response = await backend.post(`/list_entries`, { data });
    dispatch({ type: LIST_ENTRIES, payload: response.data });
  };
};

export const scratchEntry = (id) => {
  return async () => {
    await backend.get(`/scratch_entry/${id}`);
  };
};

export const fetchLivePrediction = (data) => {
  return async (dispatch) => {
    const response = await backend.post(`/get_live_prediction`, { data });
    dispatch({ type: FETCH_LIVE_PREDICTION, payload: response.data });
  };
};

export const clearLivePredictions = () => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_LIVE_PREDICTIONS, payload: null });
  };
};

export const fetchRacePastPerformances = (race_id) => {
  return async (dispatch) => {
    const response = await backend.get(`/races/${race_id}/past_performances`);
    dispatch({ type: FETCH_RACE_PAST_PERFORMANCE, payload: response.data})
  }
}

export const fetchLiveOdds = (race_id) => {
  return async (dispatch) => {
    const response = await backend.get(`/races/${race_id}/live_odds`);
    dispatch({ type: FETCH_LIVE_ODDS, payload: response.data});
    return response.data;
  }
}

export const clearLiveOdds = (race_id) => {
  return async (dispatch) => {
    dispatch({ type: CLEAR_LIVE_ODDS, payload: null})
  }
}

export const fetchSimulcastRaces = () => {
  return async (dispatch) => {
    const response =  await backend.get(`/races/order_by_time`);
    dispatch({ type: FETCH_SIMULCAST_RACES, payload: response.data})
  }
}