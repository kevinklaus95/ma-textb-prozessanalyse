import 'bootstrap/dist/css/bootstrap.css';
import getCookie from './Helper/getCookie'
import {buildDictionaryBarData, buildTopicBarData} from './Helper/charts'
import React from 'react'
import TextField from 'material-ui/TextField'
import RaisedButton from 'material-ui/RaisedButton'
import axios from "axios";
import 'bootstrap/dist/css/bootstrap.css';


/* In dieser Teilkomponente soll es dem Nutzer möglich gemacht werden, einen Freitext einzugeben und diesen unabhängig
   von der Datenbank und den existierenden Fällen analysieren zu lassen.
 */
const CustomAnalysis = (props) => {
    const {state, setState} = props

    // Funktion zum Abfeuern des Calls an den Server, POST-Request bei dem der Text und die Config gesendet wird
    const startCustomAnalysis = () => {
        this.setState({loading: true})
        let config = {
            headers: {
                "X-CSRFToken": getCookie('csrftoken'),
            }
        }
        axios.post('start-custom-analysis/', {
            customText: this.state.customText,
            config: this.state.config
        }, config)
            // das Ergebnis wird abgefangen und genauso behandelt wie bei der normalen Analyse
            .then(res => this.setState({
                comments: res.data['hours'],
                ldaResult: res.data['lda_result'],
                dictionaryResult: res.data['dictionary_result'],
                loading: false
            }, () => {
                buildTopicBarData(res.data['lda_result'].entries, res.data['lda_result'].topics, false, setState, state)
                buildDictionaryBarData(res.data['dictionary_result'], false, setState, state)
            }))
            .catch(err => {this.setState({loading: false}); alert(err)});
    }

    return(
        <div className="row">
            <div className="col-md-6">
                <TextField floatingLabelText={"Freitext"} onChange={(e, newValue) => {
                    setState({customText: newValue})
                }} value={state.customText}
                           multiLine
                           rows={3}
                />
            </div>
            <div className="col-md-3">
                <RaisedButton style={{marginTop: '20px', width: '100%'}} disabled={state.loading}
                              label={state.loading ? 'Warte auf Antwort...' : "Freitext analysieren"}
                              onClick={() => {
                                  startCustomAnalysis()
                              }}/>
            </div>
        </div>
    )
}

export default CustomAnalysis;