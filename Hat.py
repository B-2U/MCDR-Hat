from mcdreforged.api.all import *
import json

PLUGIN_METADATA = {
	'id': 'hat',
	'version': '1.0.0',
	'name': '!!hat',
	'author': '_GieR',
	'link': 'https://github.com/alexkao1439/MCDR-Hat',
	'dependencies': {
		'minecraft_data_api': '*',
	}
}


@new_thread(PLUGIN_METADATA['name'])
def put_on(source: CommandSource):
	if isinstance(source, PlayerCommandSource):
		api = source.get_server().get_plugin_instance('minecraft_data_api')
		
		selected_slot = api.get_player_info(source.player,'SelectedItemSlot')
		selected_slotinfo = [i for i in api.get_player_info(source.player,'Inventory') if i['Slot'] == selected_slot]
		if not len(selected_slotinfo):
			selected_slotinfo = None
		
		head_slotinfo = [i for i in api.get_player_info(source.player,'Inventory') if i['Slot'] == 103]
		if not len(head_slotinfo):
			head_slotinfo = None

		item1 = slot_item_decode(selected_slotinfo[0])
		item2 = slot_item_decode(head_slotinfo[0])
		slot1 = 'container.'+str(selected_slot)
		slot2 = 'armor.head'

		execute = source.get_server().execute
		if not item1 and not item2:
			return
		elif not item1:
			execute(pack_repitem(source.player, slot1, item2))
			execute(pack_repitem(source.player, slot2, item_air()))
		elif not item2:
			execute(pack_repitem(source.player, slot1, item_air()))
			execute(pack_repitem(source.player, slot2, item1))
		else:
			execute(pack_repitem(source.player, slot2, item1))
			execute(pack_repitem(source.player, slot1, item2))

def pack_repitem(player, slot, item):
        return 'replaceitem entity ' + player + ' ' + str(slot) + ' ' + item[
            'id'] + item['tag'] + ' ' + str(item['count'])

def slot_item_decode(info):
        count = info['Count']
        id = info['id']
        tag = json.dumps(info['tag']) if 'tag' in info else ''
        return {'count': count, 'id': id, 'tag': tag}

def item_air():
        return {'id': 'minecraft:air', 'count': 1, 'tag': ''}

def on_load(server: ServerInterface, prev):
	server.register_help_message('!!hat', '把手上的物品戴到頭上')
	server.register_command(Literal('!!hat').runs(put_on))
