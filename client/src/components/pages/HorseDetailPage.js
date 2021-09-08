import React from "react";
import { connect } from "react-redux";

import { ResultLines, PastPerformanceLines } from "../utils";
import {
  fetchHorse,
  queryResults,
  fetchPastPerformances,
  clearHorse,
  clearResults,
  clearPastPerformances,
} from "../../actions";

import "../../styles/styles.css";

class HorseDetailPage extends React.Component {
  componentDidMount() {
    const { id } = this.props.match.params;
    this.props.fetchHorse(id);
    this.props.fetchPastPerformances(id);
    this.props.queryResults([
      {
        field: "horse_id",
        operator: "eq",
        arguments: [id],
      },
    ]);
  }

  componentWillUnmount() {
    this.props.clearHorse();
    this.props.clearResults();
    this.props.clearPastPerformances();
  }

  breedingInfo(horse) {
    let text = "Bred in ";
    if (!!horse.location_born) {
      text += horse.location_born.toUpperCase();
    } else {
      text += "unkown";
    }
    if (!!horse.breeder) {
      text += ` by ${horse.breeder}`;
    }
    if (!!horse.year_born) {
      text += ` in ${horse.year_born}`;
    }
    return text;
  }

  saleInfo(horse) {
    if (!!horse.sale_year) {
      return `Sale: Sold for $${horse.sale_price}k in '${horse.sale_year} at ${horse.sale_location}`;
    }
  }

  studInfo(horse) {
    if (!!horse.stud_fee) {
      return `Stud Fee: $${horse.stud_fee}k`;
    }
  }

  renderedHorseInfo() {
    const horse = this.props.horse;
    if (horse.name === undefined) {
      return null;
    }
    return (
      <div>
        <div className="ui segment">
          <div>
            <h2 className="ui header center aligned">
              {horse.name.toUpperCase()}
            </h2>
          </div>
          <div>
            <div>Sire: {horse.sire.toUpperCase()}</div>
            <div>Dam: {horse.dam.toUpperCase()}</div>
            <div>{this.saleInfo(horse)}</div>
            <div>{this.studInfo(horse)}</div>
            <div>{this.breedingInfo(horse)}</div>
          </div>
        </div>
      </div>
    );
  }

  render() {
    const { id } = this.props.match.params;
    let pastPerformances;
    if (this.props.pastPerformances[id]) {
      pastPerformances = this.props.pastPerformances[id]
    } else {
      pastPerformances = []
    }
    return (
      <div>
        <div>{this.renderedHorseInfo()}</div>
        <h2>Results</h2>
        <ResultLines
          headers={[
            "track_code",
            "race_date",
            "race_number",
            "distance",
            "surface",
            "program_number",
            "trainer",
            "jockey",
            "owner",
          ]}
          results={this.props.results}
        />
        <h2>Past Performances</h2>
        <PastPerformanceLines
          pastPerformances={pastPerformances}
          headers={[
            "track_code",
            "race_date",
            "race_number",
            "distance",
            "surface",
          ]}
        />
      </div>
    );
  }
}

const mapStatetoProps = (state) => {
  return {
    horse: state.backend.horse,
    results: state.backend.results,
    pastPerformances: state.backend.pastPerformances,
  };
};

export default connect(mapStatetoProps, {
  fetchHorse,
  queryResults,
  fetchPastPerformances,
  clearHorse,
  clearResults,
  clearPastPerformances,
})(HorseDetailPage);
