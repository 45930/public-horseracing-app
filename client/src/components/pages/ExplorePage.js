import React from "react";
import { connect } from "react-redux";
import { Dropdown } from "semantic-ui-react";

import { mean } from "mathjs";

import { ResultLines } from "../utils";
import {
  queryResults,
  indexJockeys,
  indexTrainers,
  indexTracks,
  clearResults,
} from "../../actions";

import "../../styles/styles.css";

class ExplorePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filter: {
        date: {},
        track: [],
        trainer: [],
        jockey: [],
        surface: [],
        distance: {},
      },
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentWillMount() {
    this.props.queryResults(this.buildFilter());
    this.props.indexJockeys();
    this.props.indexTrainers();
    this.props.indexTracks();
  }

  componentWillUnmount() {
    this.props.clearResults();
  }

  handleFilterEvent(field, e) {
    const filter = this.state.filter;
    const fieldElements = field.split(">");
    let pointer = filter;
    let current_el;
    for (const el of fieldElements) {
      if (!!current_el) {
        pointer = pointer[current_el];
      }
      current_el = el;
    }
    pointer[current_el] = e.target.value;
    this.setState({
      filter,
    });
  }

  handleDropdownChange(field, event, { value }) {
    const filter = this.state.filter;
    filter[field] = value;
    this.setState({
      filter,
    });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.queryResults(this.buildFilter());
  }

  handleMultiSelect(field, e) {
    var options = e.target.options;
    var value = [];
    for (var i = 0, l = options.length; i < l; i++) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }
    this.setState({ value: value });
  }

  buildFilter() {
    const stateElements = this.state.filter;
    let filter = [];
    if (Object.keys(stateElements.date).length > 0) {
      if (stateElements.date["min"] !== undefined) {
        filter.push({
          field: "date",
          operator: "gte",
          arguments: [stateElements.date["min"]],
        });
      }
      if (stateElements.date["max"] !== undefined) {
        filter.push({
          field: "date",
          operator: "lte",
          arguments: [stateElements.date["max"]],
        });
      }
    }
    if (stateElements.track.length > 0) {
      filter.push({
        field: "track_id",
        operator: "in",
        arguments: stateElements.track,
      });
    }
    if (stateElements.trainer.length > 0) {
      filter.push({
        field: "trainer_id",
        operator: "in",
        arguments: stateElements.trainer,
      });
    }
    if (stateElements.jockey.length > 0) {
      filter.push({
        field: "jockey_id",
        operator: "in",
        arguments: stateElements.jockey,
      });
    }
    if (stateElements.surface.length > 0) {
      filter.push({
        field: "surface",
        operator: "in",
        arguments: stateElements.surface,
      });
    }
    if (Object.keys(stateElements.distance).length > 0) {
      if (stateElements.distance["min"] !== undefined) {
        filter.push({
          field: "distance",
          operator: "gte",
          arguments: [stateElements.distance["min"]],
        });
      }
      if (stateElements.distance["max"] !== undefined) {
        filter.push({
          field: "distance",
          operator: "lte",
          arguments: [stateElements.distance["max"]],
        });
      }
    }
    return filter;
  }

  renderedFilters() {
    return (
      <div className="ui form">
        <div className="ui two column stackable grid">
          <div className="column">
            <div className="field">
              <label>
                Start Date:
                <input
                  type="date"
                  value={this.state.filter.date.min}
                  onChange={this.handleFilterEvent.bind(this, "date>min")}
                ></input>
              </label>
            </div>
          </div>
          <div className="column">
            <div className="field">
              <label>
                End Date:
                <input
                  type="date"
                  value={this.state.filter.date.max}
                  onChange={this.handleFilterEvent.bind(this, "date>max")}
                ></input>
              </label>
            </div>
          </div>
          <div className="four column row">
            <div className="column">
              <div className="field">
                <label>Tracks</label>
                <Dropdown
                  placeholder="Select Tracks"
                  fluid
                  search
                  selection
                  multiple
                  options={this.props.trackIndex.map((track) => {
                    return {
                      key: track.id,
                      value: track.id,
                      text: track.code,
                    };
                  })}
                  onChange={this.handleDropdownChange.bind(this, "track")}
                />
              </div>
            </div>
            <div className="column">
              <div className="field">
                <label>Trainers</label>
                <Dropdown
                  placeholder="Select Trainer"
                  fluid
                  search
                  selection
                  multiple
                  options={this.props.trainerIndex.map((trainer) => {
                    return {
                      key: trainer.id,
                      value: trainer.id,
                      text: trainer.full_name,
                    };
                  })}
                  onChange={this.handleDropdownChange.bind(this, "trainer")}
                />
              </div>
            </div>
            <div className="column">
              <div className="field">
                <label>Jockeys</label>
                <Dropdown
                  placeholder="Select Jockey"
                  fluid
                  search
                  selection
                  multiple
                  options={this.props.jockeyIndex.map((jockey) => {
                    return {
                      key: jockey.id,
                      value: jockey.id,
                      text: jockey.full_name,
                    };
                  })}
                  onChange={this.handleDropdownChange.bind(this, "jockey")}
                />
              </div>
            </div>
            <div className="column">
              <div className="field">
                <label>Surface</label>
                <Dropdown
                  placeholder="Select Surface"
                  fluid
                  search
                  selection
                  multiple
                  options={[
                    {
                      key: "d",
                      value: "d",
                      text: "Dirt",
                    },
                    {
                      key: "t",
                      value: "t",
                      text: "Turf",
                    },
                  ]}
                  onChange={this.handleDropdownChange.bind(this, "surface")}
                />
              </div>
            </div>
          </div>
          <div className="column">
            <div className="field">
              <label>
                Min Distance
                <input
                  type="number"
                  value={this.state.filter.distance.min}
                  onChange={this.handleFilterEvent.bind(this, "distance>min")}
                />
              </label>
            </div>
          </div>
          <div className="column">
            <div className="field">
              <label>
                Max Distance
                <input
                  type="number"
                  value={this.state.filter.distance.max}
                  onChange={this.handleFilterEvent.bind(this, "distance>max")}
                />
              </label>
            </div>
          </div>
          <div className="row">
            <div className="column">
              <button onClick={this.handleSubmit}>Update Filter</button>
            </div>
          </div>
        </div>
        <div className="ui divider"></div>
      </div>
    );
  }

  renderedStats() {
    const results = this.props.results;
    let wins = 0;
    let starts = results.length;
    let odds = [];
    let winning_odds = [];
    this.props.results.forEach((result) => {
      odds.push(result.odds);
      if (result.final_position === 1) {
        wins += 1;
        winning_odds.push(result.odds);
      }
    });
    let meanOdds;
    let meanWinningOdds;
    let roi;
    if (starts > 0) {
      meanOdds = (mean(odds) / 100).toFixed(2);
      if (wins > 0) {
        meanWinningOdds = (mean(winning_odds) / 100).toFixed(2);
      } else {
        meanWinningOdds = 0;
      }
      roi = ((2 * ((meanWinningOdds + 1) * wins)) / starts).toFixed(2);
    }
    return (
      <div className="ui stackable grid">
        <div className="ui three wide column">
          <div className="ui segment">
            <div className="content">Starts: {starts}</div>
          </div>
        </div>
        <div className="ui two wide column">
          <div className="ui segment">
            <div className="content">Wins: {wins}</div>
          </div>
        </div>
        <div className="ui four wide column">
          <div className="ui segment">
            <div className="content">Average Odds: {meanOdds}</div>
          </div>
        </div>
        <div className="ui four wide column">
          <div className="ui segment">
            <div className="content">
              Avereage Winning Odds: {meanWinningOdds}
            </div>
          </div>
        </div>
        <div className="ui three wide column">
          <div className="ui segment">
            <div className="content">$2 ROI: {roi}</div>
          </div>
        </div>
      </div>
    );
  }

  render() {
    return (
      <div className="ui container">
        {this.renderedFilters()}
        {this.renderedStats()}
        <div className="ui divider"></div>
        <div>
          <h2 className="ui header">Results with Filter</h2>
          <ResultLines
            headers={[
              "track_code",
              "race_date",
              "distance",
              "surface",
              "horse_name",
              "trainer",
              "jockey",
            ]}
            results={this.props.results}
          />
        </div>
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    results: state.backend.results,
    jockeyIndex: state.backend.jockeyIndex,
    trainerIndex: state.backend.trainerIndex,
    trackIndex: state.backend.trackIndex,
  };
};

export default connect(mapStatetoProps, {
  queryResults,
  indexJockeys,
  indexTrainers,
  indexTracks,
  clearResults,
})(ExplorePage);
