import {
  FETCH_CARDS,
  FETCH_HORSE,
  FETCH_RACE,
  FETCH_TRAINER,
  FETCH_JOCKEY,
  FETCH_OWNER,
  FETCH_TRAINER_STATS,
  FETCH_JOCKEY_STATS,
  FETCH_OWNER_STATS,
  FETCH_PAST_PERFORMANCES,
  FETCH_RACE_PAST_PERFORMANCE,
  QUERY_RESULTS,
  INDEX_JOCKEYS,
  INDEX_TRAINERS,
  INDEX_TRACKS,
  QUERY_CARDS,
  FETCH_ENTRANTS,
  SEARCH_HORSES,
  FETCH_HOT_JOCKEYS,
  FETCH_HOT_TRAINERS,
  CLEAR_RESULTS,
  CLEAR_JOCKEY,
  CLEAR_TRAINER,
  CLEAR_OWNER,
  CLEAR_RACE,
  CLEAR_PAST_PERFORMANCES,
  CLEAR_CARDS,
  CLEAR_HORSE,
  CLEAR_HOT_JOCKEYS,
  CLEAR_HOT_TRAINERS,
  LIST_ENTRIES,
  CLEAR_ENTRANTS,
  FETCH_LIVE_PREDICTION,
  CLEAR_LIVE_PREDICTIONS,
  FETCH_LIVE_ODDS,
  CLEAR_LIVE_ODDS,
  FETCH_SIMULCAST_RACES
} from "../actions/actionTypes";

const INITIAL_STATE = {
  cards: [],
  race: {},
  trainer: {
    info: {},
    stats: {
      track_stats: [],
      jockey_stats: [],
      class_stats: [],
      surface_stats: [],
    },
  },
  jockey: {
    info: {},
    stats: {
      track_stats: [],
      trainer_stats: [],
      class_stats: [],
      surface_stats: [],
    },
  },
  owner: {
    info: {},
    stats: {
      trainer_stats: [],
      jockey_stats: [],
      class_stats: [],
      surface_stats: [],
    },
  },
  results: [],
  horse: {},
  trainerIndex: [],
  jockeyIndex: [],
  trackIndex: [],
  pastPerformances: {},
  entrants: [],
  horse_search_results: [],
  hot_jockeys: [],
  hot_trainers: [],
  entries: [],
  live_predictions: [],
  liveOdds: {},
  simulcastRaces: []
};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case FETCH_CARDS:
      return { ...state, cards: action.payload };
    case FETCH_HORSE:
      return { ...state, horse: action.payload };
    case FETCH_RACE:
      return { ...state, race: action.payload };
    case FETCH_TRAINER:
      return { ...state, trainer: { ...state.trainer, info: action.payload } };
    case FETCH_JOCKEY:
      return { ...state, jockey: { ...state.jockey, info: action.payload } };
    case FETCH_OWNER:
      return { ...state, owner: { ...state.owner, info: action.payload } };
    case FETCH_TRAINER_STATS:
      return { ...state, trainer: { ...state.trainer, stats: action.payload } };
    case FETCH_JOCKEY_STATS:
      return { ...state, jockey: { ...state.jockey, stats: action.payload } };
    case FETCH_OWNER_STATS:
      return { ...state, owner: { ...state.owner, stats: action.payload } };
    case FETCH_PAST_PERFORMANCES:
      return {
        ...state,
        pastPerformances: {...action.payload},
      };
    case FETCH_RACE_PAST_PERFORMANCE:
      return {
        ...state,
        pastPerformances: action.payload,
      };
    case QUERY_RESULTS:
      return { ...state, results: action.payload };
    case INDEX_JOCKEYS:
      return { ...state, jockeyIndex: action.payload };
    case INDEX_TRAINERS:
      return { ...state, trainerIndex: action.payload };
    case INDEX_TRACKS:
      return { ...state, trackIndex: action.payload };
    case QUERY_CARDS:
      return { ...state, cards: action.payload };
    case FETCH_ENTRANTS:
      return {
        ...state,
        entrants: action.payload,
      };
    case SEARCH_HORSES:
      return {
        ...state,
        horse_search_results: action.payload,
      };
    case FETCH_HOT_JOCKEYS:
      return {
        ...state,
        hot_jockeys: action.payload,
      };
    case FETCH_HOT_TRAINERS:
      return {
        ...state,
        hot_trainers: action.payload,
      };
    case CLEAR_RESULTS:
      return {
        ...state,
        results: [],
      };
    case CLEAR_JOCKEY:
      return {
        ...state,
        jockey: {
          info: {},
          stats: {
            track_stats: [],
            trainer_stats: [],
            class_stats: [],
            surface_stats: [],
          },
        },
      };
    case CLEAR_TRAINER:
      return {
        ...state,
        trainer: {
          info: {},
          stats: {
            track_stats: [],
            jockey_stats: [],
            class_stats: [],
            surface_stats: [],
          },
        },
      };
    case CLEAR_OWNER:
      return {
        ...state,
        owner: {
          info: {},
          stats: {
            trainer_stats: [],
            jockey_stats: [],
            class_stats: [],
            surface_stats: [],
          },
        },
      };
    case CLEAR_RACE:
      return {
        ...state,
        race: {},
      };
    case CLEAR_PAST_PERFORMANCES:
      return {
        ...state,
        pastPerformances: {},
      };
    case CLEAR_CARDS:
      return {
        ...state,
        cards: [],
      };
    case CLEAR_HORSE:
      return {
        ...state,
        horse: {},
      };
    case CLEAR_HOT_JOCKEYS:
      return {
        ...state,
        hot_jockeys: [],
      };
    case CLEAR_HOT_TRAINERS:
      return {
        ...state,
        hot_trainers: [],
      };
    case LIST_ENTRIES:
      return {
        ...state,
        entries: action.payload,
      };
    case CLEAR_ENTRANTS:
      return {
        ...state,
        entrants: [],
      };
    case FETCH_LIVE_PREDICTION:
      return {
        ...state,
        live_predictions: action.payload,
      };
    case CLEAR_LIVE_PREDICTIONS:
      return {
        ...state,
        live_predictions: [],
      };
    case FETCH_LIVE_ODDS:
      return {
        ...state,
        live_odds: action.payload,
      };
    case CLEAR_LIVE_ODDS:
      return {
        ...state,
        live_odds: {},
      };
    case FETCH_SIMULCAST_RACES:
      return {
        ...state,
        simulcastRaces: action.payload
      };
    default:
      return state;
  }
};
