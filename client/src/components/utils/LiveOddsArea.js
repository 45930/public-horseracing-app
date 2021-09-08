import React from "react";
import { connect } from "react-redux";

import { fetchLivePrediction, clearLivePredictions } from "../../actions";

import "../../styles/styles.css";

class LiveOddsArea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      liveOdds: {},
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentWillUnmount() {
    this.props.clearLivePredictions();
  }

  handleInput(result_id, e) {
    e.preventDefault();
    const { liveOdds } = this.state;
    liveOdds[result_id] = e.target.value;
    this.setState({ liveOdds });
  }

  handleSubmit(e) {
    this.props.fetchLivePrediction({
      raceId: this.props.raceId,
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
      <div className="bottom-div">
        <button onClick={this.handleSubmit}>Get Updated Predictions</button>
        {this.renderedPredictionOutput()}
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    live_predictions: state.backend.live_predictions,
  };
};

export default connect(mapStatetoProps, {
  fetchLivePrediction,
  clearLivePredictions,
})(LiveOddsArea);
