import React from "react";
import { connect } from "react-redux";

import { ResultLines, StatisticTable, TimeFrameSelector } from "../utils";
import {
  fetchJockey,
  fetchJockeyStats,
  queryResults,
  clearJockey,
  clearResults,
} from "../../actions";

class JockeyDetailPage extends React.Component {
  constructor(props) {
    super(props);
    this.onTimeFrameSelect = this.onTimeFrameSelect.bind(this);
  }

  componentDidMount() {
    const { id } = this.props.match.params;
    this.props.fetchJockey(id);
    this.props.fetchJockeyStats(id, 90);
    this.props.queryResults([
      {
        field: "jockey_id",
        operator: "eq",
        arguments: [id],
      },
    ]);
  }

  componentWillUnmount() {
    this.props.clearJockey();
    this.props.clearResults();
  }

  onTimeFrameSelect(e, { name }) {
    this.props.clearJockey();
    const { id } = this.props.match.params;
    this.props.fetchJockey(id);
    if (name === "all_time") {
      this.props.fetchJockeyStats(id);
    } else {
      this.props.fetchJockeyStats(id, parseInt(name));
    }
  }

  routeText(route) {
    if (route === 1) {
      return "Route";
    } else {
      return "Sprint";
    }
  }

  winRate() {
    let wins = 0;
    let starts = 0;
    this.props.jockey.stats.surface_stats.forEach((surface) => {
      wins += surface.wins;
      starts += surface.starts;
    });
    if (starts > 0) {
      return Math.round((wins * 100) / starts, 2);
    } else {
      return 0;
    }
  }

  renderedPlaceholder() {
    return (
      <div className="ui placeholder">
        <div className="paragraph">
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
          <div className="line"></div>
        </div>
      </div>
    );
  }

  renderedStats() {
    if (this.props.jockey.stats.track_stats.length > 0) {
      return (
        <div className="four column row">
          <div className="column">
            <StatisticTable
              title="Track"
              data={this.props.jockey.stats.track_stats.map((stat) => ({
                ...stat,
                feature_name: stat.track_code,
              }))}
            />
          </div>
          <div className="column">
            <StatisticTable
              title="Trainer"
              data={this.props.jockey.stats.trainer_stats.map((stat) => ({
                ...stat,
                feature_name: stat.full_name,
              }))}
            />
          </div>
          <div className="column">
            <StatisticTable
              title="Class"
              data={this.props.jockey.stats.class_stats.map((stat) => ({
                ...stat,
                feature_name: stat.classification,
              }))}
            />
          </div>
          <div className="column">
            <StatisticTable
              title="Surface"
              data={this.props.jockey.stats.surface_stats.map((stat) => ({
                ...stat,
                feature_name: `${stat.surface} - ${this.routeText(stat.route)}`,
              }))}
            />
          </div>
        </div>
      );
    } else {
      return (
        <div className="four column row">
          <div className="column">{this.renderedPlaceholder()}</div>
          <div className="column">{this.renderedPlaceholder()}</div>
          <div className="column">{this.renderedPlaceholder()}</div>
          <div className="column">{this.renderedPlaceholder()}</div>
        </div>
      );
    }
  }

  render() {
    return (
      <div>
        <div className="ui stackable grid">
          <div className="row">
            <div className="six wide column">
              <h2 className="ui header left floated">Name</h2>
              <div>{this.props.jockey.info.full_name}</div>
            </div>
            <div className="six wide column right floated">
              <div className="row">
                <h2 className="ui header left floated">Win %</h2>
                <div className="ui right floated content">{this.winRate()}</div>
              </div>
            </div>
          </div>
          <div className="row">
            <TimeFrameSelector onClick={this.onTimeFrameSelect} />
          </div>
          {this.renderedStats()}
        </div>
        <h2 className="ui header">Recent Results</h2>
        <ResultLines
          headers={[
            "track_code",
            "race_date",
            "race_number",
            "distance",
            "surface",
            "program_number",
            "horse_name",
            "trainer",
            "owner",
          ]}
          results={this.props.results}
        />
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    jockey: state.backend.jockey,
    results: state.backend.results,
  };
};

export default connect(mapStatetoProps, {
  fetchJockey,
  fetchJockeyStats,
  queryResults,
  clearJockey,
  clearResults,
})(JockeyDetailPage);
