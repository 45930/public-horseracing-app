import React from "react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";

import { ResultLines, LiveOddsArea } from "../utils";
import {
  fetchRace,
  queryEntrants,
  fetchRacePastPerformances,
  fetchLiveOdds,
  fetchLivePrediction,
  clearRace,
  clearEntrants,
  clearPastPerformances,
  clearLiveOdds,
  clearLivePredictions,
} from "../../actions";

import "../../styles/styles.css";

class RaceDetailPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = { 
      id: this.props.match.params.id,
      liveOdds: this.props.liveOdds
    };
    this.handleUpdateLiveOdds = this.handleUpdateLiveOdds.bind(this)
    this.updateLiveOdds = this.updateLiveOdds.bind(this)
    this.requestPredictions = this.requestPredictions.bind(this)
  }

  componentDidMount() {
    const { id } = this.props.match.params;
    this.props.fetchRace(id);
    this.props.queryEntrants([
      {
        field: "race_id",
        operator: "eq",
        arguments: [id],
      },
    ]);
    this.props.fetchRacePastPerformances(id);
  }

  componentDidUpdate() {
    const { id } = this.props.match.params;
    if (this.state.id !== id) {
      this.setState({id: id})
      this.props.fetchRace(id);
      this.props.queryEntrants([
        {
          field: "race_id",
          operator: "eq",
          arguments: [id],
        },
      ]);
      this.props.fetchRacePastPerformances(id);
    }

  }

  componentWillUnmount() {
    this.props.clearRace();
    this.props.clearEntrants();
    this.props.clearPastPerformances();
    this.props.clearLiveOdds();
  }

  handleUpdateLiveOdds(resultId, event) {
    event.preventDefault();
    const { liveOdds } = this.state;
    liveOdds[resultId] = event.target.value;
    this.setState({ liveOdds });
  }

  renderedClass(race_class) {
    let classText;

    switch (race_class) {
      case "mcl":
        classText = "Maiden Claiming";
        break;
      case "gstk":
        classText = "Graded Stakes";
        break;
      case "an2l":
        classText = "Allowance, Non-Winners of Two";
        break;
      case "clm":
        classText = "Claimimg";
        break;
      case "ocln":
        classText = "Allowance Optional Claiming Non-Winners of One";
        break;
      case "stk":
        classText = "Overnight Stakes";
        break;
      case "soc":
        classText = "Starter Allowance Optional Claiming";
        break;
      case "clmn":
        classText = "Claiming Non-Winners of One";
        break;
      case "str":
        classText = "Starter Allowance";
        break;
      case "msw":
        classText = "Maiden Special Weight";
        break;
      case "aoc":
        classText = "Allowance Optional Claiming";
        break;
      case "alw":
        classText = "Allowance";
        break;
      case "an3l":
        classText = "Allowance Non-Winners of Three";
        break;
      case "mdn":
        classText = "Maiden";
        break;
      default:
        classText = race_class;
    }
    return classText;
  }

  restrictionText(age, sex, state) {
    let ageText;
    let sexText;
    let stateText;
    switch (age) {
      case "31":
        ageText = "Three year olds and up";
        break;
      case "21":
        ageText = "Two year olds and up";
        break;
      case "3":
        ageText = "Three year olds";
        break;
      case "2":
        ageText = "Two year olds";
        break;
      default:
        ageText = age;
        break;
    }
    switch (sex) {
      case "o":
        sexText = ", open company";
        break;
      case "m":
        sexText = ", fillies and mares";
        break;
      case "f":
        sexText = ", fillies";
        break;
      default:
        sexText = `, ${sex}`;
        break;
    }
    if (!!state) {
      stateText = ", statebred";
    } else {
      stateText = "";
    }
    return ageText.concat(sexText, stateText);
  }

  renderedClaimPrice() {
    const race = this.props.race;
    if (!!race.claim_price) {
      return <div>Claim Price: ${race.claim_price}k</div>;
    } else {
      return "";
    }
  }

  renderedRaceInfo() {
    const race = this.props.race;
    if (race.track_code === undefined) {
      return null;
    }
    return (
      <div className="ui segment">
        <div>
          <h2 className="ui header center aligned">
            {race.track_code.toUpperCase() +
              " - " +
              race.date +
              " Race " +
              race.race_number}
          </h2>
        </div>
        <div>
          <div>Post Time: {race.post_time}</div>
          <div>Class: {this.renderedClass(race.classification)}</div>
          <div>Purse: ${race.purse}k</div>
          {this.renderedClaimPrice()}
          <div>Distance: {race.distance}f</div>
          <div>Surface: {race.surface}</div>
          <div>
            Restrictions:{" "}
            {this.restrictionText(
              race.age_restrictions,
              race.sex_restrictions,
              race.is_state_bred
            )}
          </div>
        </div>
      </div>
    );
  }

  renderedRaceNav() {
    const nextRaceId = String(parseInt(this.props.match.params.id) + 1);
    const prevRaceId = String(parseInt(this.props.match.params.id) - 1);
    return(<div className="ui segment">
      <Link to={`/races/${prevRaceId}`}>
        Previous Race
      </Link>
      <Link to={`/races/${nextRaceId}`}>
        Next Race
      </Link>
    </div>)
  }

  renderedLiveOddsSection() {
    const { results } = this.props;
    if (results.length > 0) {
      if (results.every((r) => r.final_position === null)) {
        return <LiveOddsArea results={results} raceId={this.props.race.id} />;
      }
    }
  }

  async updateLiveOdds() {
    const {id} = this.props.match.params;
    const data = await this.props.fetchLiveOdds(id);
    this.setState({liveOdds: data});
  }

  requestPredictions(e) {
    this.props.fetchLivePrediction({
      raceId: this.props.match.params.id,
      liveOdds: this.state.liveOdds,
    });
  }

  renderedOutput(prediction) {
    return (
      <tr key={prediction.result_id}>
        <td data-label="Program Nmber">{prediction.program_number}</td>
        <td data-label="Horse Name">{prediction.horse_name}</td>
        <td data-label="Implied Prob">{prediction.implied_proba}</td>
        <td data-label="Win Prob">{prediction.live_pred_win_probability}</td>
      </tr>
    );
  }

  renderedPredictionOutput() {
    if (this.props.live_predictions.length === 0) {
      return <div>Prediction will go here when it is ready</div>;
    } else {
      return (
        <table className="ui basic compact unstackable table">
          <thead>
            <tr>
              <th>Program Number</th>
              <th>Horse Name</th>
              <th>Implied Prob</th>
              <th>Win Prob</th>
            </tr>
          </thead>
          <tbody>
            {this.props.live_predictions.map((live_prediction) => {
              return this.renderedOutput(live_prediction);
            })}
          </tbody>
        </table>
      );
    }
  }

  render() {
    return (
      <div>
        <div>{this.renderedRaceInfo()}</div>
        <div>{this.renderedRaceNav()}</div>
        <button onClick={this.updateLiveOdds}>Update with Live Odds</button>
        <ResultLines
          headers={[
            "program_number",
            "horse_name",
            "trainer",
            "jockey",
            "owner",
          ]}
          results={this.props.results}
          pastPerformances={this.props.pastPerformances}
          liveOdds={this.state.liveOdds}
          liveOddsUpdate={this.handleUpdateLiveOdds}
        />
        <div className="bottom-div">
          <button onClick={this.requestPredictions}>Get Updated Predictions</button>
          {this.renderedPredictionOutput()}
        </div>
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    race: state.backend.race,
    results: state.backend.results,
    pastPerformances: state.backend.pastPerformances,
    liveOdds: state.backend.liveOdds,
    live_predictions: state.backend.live_predictions,
  };
};

export default connect(mapStatetoProps, {
  fetchRace,
  queryEntrants,
  fetchRacePastPerformances,
  fetchLiveOdds,
  fetchLivePrediction,
  clearRace,
  clearEntrants,
  clearPastPerformances,
  clearLiveOdds,
  clearLivePredictions,
})(RaceDetailPage);
