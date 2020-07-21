import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';
import GraphElement from './GraphElement';

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
      result: "",
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
  triggerGraphRender = (data) => {
    alert("Creating graph")
    this.setState({
      graphIsVisible: true,
      result: JSON.stringify(data),
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
        this.triggerGraphRender(data);
        // this.setState({
        //   result: JSON.stringify(data),
        //   isLoading: false
        // });
      });
  }

  handleCancelClick = (event) => {
    this.setState({ result: "" });
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
                  <option>2020-08-20</option>
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
                  <option>Calls</option>
                  <option>Puts</option>
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
                  <option>Credit</option>
                  <option>Debit</option>
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
          {result === "" ? null :
            (<Row>
              <Col className="result-container">
                <h5 id="result">{result}</h5>
              </Col>
            </Row>)
          }
          {this.state.graphIsVisible ? <GraphElement xaxis={this.state.xaxis} yaxis={this.state.yaxis}/> : ""}
        </div>
      </Container>
    );
  }
}

export default App;
