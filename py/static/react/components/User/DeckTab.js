import React from 'react'
import { get_decks } from '../../api/DeckService'
import { check_has_deck_temp_collection } from '../../api/UserService'
import { add_deck_to_tmp_collection } from '../../api/DeckService'
import { remove_deck_from_tmp_collection} from '../../api/DeckService'
import CurrentDecks from '../CurrentDecks'
import Show_Missing_Cards from '../Show_Missing_Cards'


export default class DeckTab extends React.Component {

	constructor(props) {
		super(props)
		this.state = {
			displayed_decks: [],
			checked_out_decks: [],
			temporary_collection: this.props.user.collection,
			has_deck_in_temp_collection: {},
			missing_cards_from_temp_collection: {},
			missing_cards: 0,
			page: 1,
			num_pages: -1
		}
		this.dropDown = ['None']
		this.filtered_decks = []
		this.all_decks = []
		this.DECKS_PER_PAGE = 10

	}

	get_decks_to_display(page){
		var form_data = {
			jwt: this.props.user.jwt,
			page: page
		}
		get_decks(form_data, this.handle_get_decks_to_display_Response.bind(this))
	}

	handle_get_decks_to_display_Response(response) {
		this.all_decks = response.decks
		this.filtered_decks = this.all_decks
		this.dropDown = this.dropDown.concat(response.dropDown)
		let decks = this.filtered_decks.slice(this.DECKS_PER_PAGE*(this.state.page-1),this.DECKS_PER_PAGE)
		this.setState({ displayed_decks: decks})
		this.setState({ num_pages: response.num_pages})
		this.filter_decks.bind(this)(decks)
	}	

	check_has_deck(deck_id){
		var form_data = {
			jwt: this.props.user.jwt,
			deck_id: deck_id,
			tmp_collection: this.state.temporary_collection,
			missing_cards: this.state.missing_cards
		}
		check_has_deck_temp_collection(form_data, this.handle_check_has_deck_response.bind(this))
		}

	handle_check_has_deck_response(response){
		var new_state = this.state.has_deck_in_temp_collection
		new_state[response.deck_id] = response.has_deck
		this.setState({has_deck_in_temp_collection: new_state})
		var second_new_state = this.state.missing_cards_from_temp_collection
		second_new_state[response.deck_id] = response.missing_from_deck
		this.setState({missing_cards_from_temp_collection: second_new_state})
	}

	add_deck(deck_id){
		var form_data = {
			jwt: this.props.user.jwt,
			deck_id: deck_id,
			temporary_collection: this.state.temporary_collection
		}
		add_deck_to_tmp_collection(form_data, this.handle_add_deck_response.bind(this))
	}

	handle_add_deck_response(response){
		this.setState({temporary_collection: response.updated_collection})
		var checked_out = this.state.checked_out_decks
		for(var x in checked_out){
			var deck = checked_out[x]
			if(response.deck.deck_id == checked_out[x]['deck_id']){
				checked_out.splice(x,1)
				break
			}
		}
		this.filter_decks(this.state.displayed_decks)
	}

	//call after adding or removing a deck to reset has_deck state?
	filter_decks(decks){
		for(var x in decks){
			var deck = decks[x]
			this.check_has_deck(deck['deck_id'])
		}
	}
	remove_deck(deck_id){
		var form_data = {
			jwt: this.props.user.jwt,
			deck_id: deck_id,
			temporary_collection: this.state.temporary_collection
		}
		remove_deck_from_tmp_collection(form_data, this.handle_remove_deck_response.bind(this))
	}

	handle_remove_deck_response(response){
		var checked_out = this.state.checked_out_decks
		checked_out.push(response.deck)
		this.setState({temporary_collection: response.updated_collection})
		this.setState({checked_out_decks: checked_out})
		this.filter_decks(this.state.displayed_decks)
	}

	change_archetype_filter(event){
		var archetype = event.target.value
		var filtered_decks = []
		if (archetype === 'None'){
			filtered_decks = this.all_decks
		}
		else{
			for (var x in this.all_decks){
			if (this.all_decks[x].archetype === archetype){
				filtered_decks.push(this.all_decks[x])
			}
		}
		}
		this.filtered_decks = filtered_decks
		this.update_page(1)
	}

	update_page(page){
		let decks = this.filtered_decks.slice(this.DECKS_PER_PAGE*(page-1),this.DECKS_PER_PAGE*page)
		this.setState({page: page})
		if (this.filtered_decks.length % this.DECKS_PER_PAGE != 0 ){
			var num_pages = Math.floor(this.filtered_decks.length/this.DECKS_PER_PAGE) + 1
		}
		else{
			var num_pages = this.filtered_decks.length/this.DECKS_PER_PAGE
		}
		this.setState({num_pages: num_pages})
		this.setState({displayed_decks: decks})
		this.filter_decks.bind(this)(decks)
	}
	componentDidMount() {
	fetch(this.get_decks_to_display.bind(this)(5))
		.then(this.get_decks_to_display.bind(this)(null))
	}

	render() {
		var tab_index = this.state.tab_index
		return (
			<div className={this.props.selected ? '' : 'hidden'}>
				<div> 
				<p className="tooltips1"> This tab contains a list of modern decks from mtgtop8.com. You can sort the decks by archetype, or you can search for the deck you want by using the prev and next page buttons below. For any given deck, the 'missing cards' button will show you all the cards that are missing from your collection that you need to complete the deck. Once you have all the cards for a deck, you will be able to click the 'complete deck' button. This button will <b><i>TEMPORARILY</i></b> remove the cards from your collection and you will have successfully checked out the deck. Nice! </p>
				<table className="table table-bordered">
					<thead>
						<tr>
							<th>Current Decks Checked Out</th>
							<th>Remove</th>
						</tr>
					</thead>
					<tbody>
							{this.state.checked_out_decks.map((deck, index) => (
								<tr>
									<td><a href = {deck.url}>{deck.name}</a></td>
									<td>
										<button type="button" onClick={() => 
											this.add_deck(deck.deck_id)
										}>
											<span className="glyphicon glyphicon-minus" />
										</button>
									</td>											
								</tr>
							))}
					</tbody>
				</table>
				<table className="table table-bordered">
					<thead>
						<tr>
							<th><span className="paddingRight">Archetype</span>
								<select  onChange={this.change_archetype_filter.bind(this)}>
									{this.dropDown.map((archetype) => (
										<option value = {archetype}>{archetype.replace("\\", "")}</option>
										))
									}
								</select>
							</th>
							<th>Url </th>
							<th>Complete Deck</th>
							<th>Missing Cards</th>
						</tr>
					</thead>
					<tbody>
							{this.state.displayed_decks.map((deck,index) => (
								<tr>
									<td>
									{deck.archetype.replace("\\", "")}
									</td>
									<td><a href = {deck.url}>{deck.name.replace("\\", "").replace("-","")}</a></td>
									<td>
										<CurrentDecks
										deck_id = {deck.deck_id}
										onUpClick = {() =>
											this.remove_deck(deck.deck_id)
										}
										has_deck = {
											this.state.has_deck_in_temp_collection[deck.deck_id]
										}
										/>
									</td>
									<td>
										<Show_Missing_Cards
											deck_id = {deck.deck_id}
											missing_cards = {this.state.missing_cards_from_temp_collection[deck.deck_id]}
										/>
									</td>											
								</tr>
							))}
					</tbody>
				</table>
				<tr>
				{this.state.page === 1 ? (<button type="button" disabled={true} className="btn btn-default disabled-button" ><span>Prev </span></button>):(
				<button type="button" className="btn btn-default" onClick={() => this.update_page(this.state.page - 1)}>
							<span> Prev </span>
					</button>
					)}
				{this.state.page >= this.state.num_pages ? (<button type="button" disabled={true} className="btn btn-default disabled-button" ><span>Next</span></button>):(
					<button type="button" className="btn btn-default" onClick={() => this.update_page(this.state.page + 1)}>
							<span > Next </span>
					</button>
					)}
					
					<span> Page: {this.state.page} / {this.state.num_pages}</span>
					
				</tr>
				</div>
			</div>
		)
	}
}