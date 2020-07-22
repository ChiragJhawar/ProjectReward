import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';
import GraphElement from './GraphElement';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/dist/styles/ag-grid.css';
import 'ag-grid-community/dist/styles/ag-theme-alpine.css';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        Stock: '',
        selectDate: 1,
        selectFlag: 1,
        selectType: 1

      },
      Current_Price: 0 ,
      Long_Premium : 0,
      Long : 0,
      Short_Premium :0,
      Short : 0,
      maxReward: 0,
      maxRisk:0,
      rR_Ratio :0,
      xaxis: [],
      yaxis: [],
      graphIsVisible: false
    };
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  }
  triggerAPIResponse = (data) => {
    console.log(data)
    this.setState({
      Current_Price: data['Current Price'],
      Long_Premium : data['Long Premium'],
      Long : data['Long(Buy)'],
      Short_Premium :data['Short Premium'],
      Short :  data['Short(Sell)'],
      maxReward: data['maxReward'],
      maxRisk:data['maxRisk'],
      rR_Ratio :data['Risk/Reward Ratio'],
      graphIsVisible: true,
      isLoading: false
    })
  }
  handlePredictClick = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    // debugger;
    // debugger;
    fetch('http://localhost:7500/api/spread/basic_spreads',
      {
        method: 'POST',
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      })
      .then(response => response.json()).then(data => {
        this.triggerAPIResponse(data);
        // this.setState({
        //   result: JSON.stringify(data),
        //   isLoading: false
        // });
      });
  }

  handleCancelClick = (event) => {
    this.setState({ 
      Current_Price: 0 ,
      Long_Premium : 0,
      Long : 0,
      Short_Premium :0,
      Short : 0,
      maxReward: 0,
      maxRisk:0,
      rR_Ratio :0,
      xaxis: [],
      yaxis: [],
      graphIsVisible: false
    });
  }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;


    return (
      <Container>
        <div>
          <h1 className="title">Welcome to Project Reward</h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Stock:</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="AAPL"
                  name="Stock"
                  value={formData.Stock}
                  onChange={this.handleChange} />
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Expiry Date</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.selectDate}
                  name="selectDate"
                  onChange={this.handleChange}>
                  <option>Please Select</option>
                  <option>2020-08-21</option>
                </Form.Control>
              </Form.Group>
            </Form.Row>

            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Option Type</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.selectFlag}
                  name="selectFlag"
                  onChange={this.handleChange}>
                  <option>Please Select</option>
                  <option>calls</option>
                  <option>puts</option>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Spread Type</Form.Label>
                <Form.Control
                  as="select"
                  value={formData.selectType}
                  name="selectType"
                  onChange={this.handleChange}>
                  <option>Please Select</option>
                  <option>credit</option>
                  <option>debit</option>
                </Form.Control>
              </Form.Group>

            </Form.Row>
            <Row>
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  { isLoading ? 'Fetching Suggestions' : 'Suggest' }
                </Button>
              </Col>
              {this.state.Current_Price === 0 ? null :
        (<Row>
          <Col className="result-container">
               <div
        className="ag-theme-alpine"
        style={{
        height: '400px',
        width: '390px' }}
      > {"\n"}
        <AgGridReact
          columnDefs={[{
        headerName: "Field", field: "field"
      }, {
        headerName: "Value", field: "sv"
      }]}
          rowData={[{
        field: "Current Price", sv: this.state.Current_Price},
        {field: "Long(Buy)", sv: this.state.Long},
        {field: "Long Premium", sv: this.state.Long_Premium},
        {field: "Short(Sell)", sv: this.state.Short},
        {field: "Short Premium", sv: this.state.Short_Premium},
        {field: "Maximum Risk", sv: this.state.maxRisk},
        {field: "Maximum Reward", sv: this.state.maxReward},
        {field: "Risk/Reward Ratio", sv: this.state.rR_Ratio}]}> 
        </AgGridReact>
      </div>
        </Col>
            </Row>)
          }
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}>
                  Reset
                </Button>
              </Col>
            </Row>
          </Form>
          {this.state.graphIsVisible ? <GraphElement xaxis={this.state.xaxis} yaxis={this.state.yaxis}/> : ""}
        </div>
      </Container>
    );
  }
}

export default App;
