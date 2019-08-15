import React from 'react'
import {
    Table,
    TableBody,
    TableHeader,
    TableHeaderColumn,
    TableRow,
    TableRowColumn,
} from 'material-ui/Table';
import moment from 'moment'
import 'bootstrap/dist/css/bootstrap.css';

/* In dieser Komponente sollen nur noch einmal die gefundenen Texte aus der Datenbank im Original dargestellt werden.
*  Da diese tendenziell eher zu groß sind, als dass sie in einer Tabelle dargestellt werden können, werden die Volltexte
*  auf Klick der Zelle in einem alert angezeigt. */
const DataTable = (props) => {
    const {state} = props

    return (
    <div className="row col-xs-6">
        <Table>
            <TableHeader
                displaySelectAll={false}
                adjustForCheckbox={false}
                enableSelectAll={false}
            >
                <TableRow>
                    <TableHeaderColumn style={{width: '10%'}}>ID</TableHeaderColumn>
                    <TableHeaderColumn style={{width: '15%'}}>Start</TableHeaderColumn>
                    <TableHeaderColumn style={{width: '15%'}}>Ende</TableHeaderColumn>
                    <TableHeaderColumn style={{width: '30%'}}>Comment</TableHeaderColumn>
                    <TableHeaderColumn style={{width: '30%'}}>Reflection</TableHeaderColumn>
                </TableRow>
            </TableHeader>
            <TableBody
                displayRowCheckbox={false}
                deselectOnClickaway={false}
                showRowHover={false}
                stripedRows={false}
            >
                {state.comments.map((comment) => {
                    return (<TableRow>
                        <TableRowColumn style={{width: '10%'}}>{comment.id}</TableRowColumn>
                        <TableRowColumn
                            style={{width: '15%'}}>{moment(comment.start).format('DD.MM.YYYY, LT')}</TableRowColumn>
                        <TableRowColumn
                            style={{width: '15%'}}>{moment(comment.stop).format('DD.MM.YYYY, LT')}</TableRowColumn>
                        <TableRowColumn style={{width: '30%'}}>{<span onClick={() => {
                            alert(comment.comment)
                        }}>{comment.comment}</span>}</TableRowColumn>
                        <TableRowColumn style={{width: '30%'}}>{<span onClick={() => {
                            alert(comment.reflection)
                        }}>{comment.reflection}</span>}</TableRowColumn>
                    </TableRow>)
                })}
            </TableBody>
        </Table>
    </div>)
}

export default DataTable;