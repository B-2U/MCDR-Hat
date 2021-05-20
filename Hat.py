from mcdreforged.api.all import *
import json

PLUGIN_METADATA = {
	'id': 'hat',
	'version': '1.0.0',
	'name': '!!hat',
	'author': '_GieR',
	'link': 'https://github.com/B-2U/MCDR-Hat',
	'dependencies': {
		'minecraft_data_api': '*',
	}
}


@new_thread(PLUGIN_METADATA['name'])
def put_on(source: CommandSource):
	api = source.get_server().get_plugin_instance('minecraft_data_api')

	selected_slot = api.get_player_info(source.player,'SelectedItemSlot')
	selected_slotinfo = [i for i in api.get_player_info(source.player,'Inventory') if i['Slot'] == selected_slot]
	if not len(selected_slotinfo):
		selected_slotinfo = None

	head_slotinfo = [i for i in api.get_player_info(source.player,'Inventory') if i['Slot'] == 103]
	if not len(head_slotinfo):
		head_slotinfo = None

	item1 = slot_item_decode(selected_slotinfo)
	item2 = slot_item_decode(head_slotinfo)
	if not item1:
		item1 = item_air()
	if not item2:
		item2 = item_air()
	slot1 = 'container.'+str(selected_slot)
	slot2 = 'armor.head'

	execute = source.get_server().execute
	execute(pack_repitem(source.player, slot2, item1))
	execute(pack_repitem(source.player, slot1, item2))

def pack_repitem(player, slot, item):
        return f'replaceitem entity {player} {str(slot)} {item["id"]}{item["tag"]} {str(item["count"])}'

def slot_item_decode(info):
    if info == None:
        return {'id': 'minecraft:air', 'count': 1, 'tag': ''}
    info = info[0]
    count = info['Count']
    id = info['id']
    tag = json.dumps(info['tag']) if 'tag' in info else ''
    return {'count': count, 'id': id, 'tag': tag}


def on_load(server: ServerInterface, prev):
	check_and_put = lambda src: put_on(source) if src.is_player else src.reply('§c該命令只能被玩家使用。')
	server.register_help_message('!!hat', '把手上的物品戴到頭上')
	server.register_command(Literal('!!hat').runs(check_and_put))
