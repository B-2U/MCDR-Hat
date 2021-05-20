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
    if not source.is_player:
        source.reply('§c該命令只能被玩家使用')
        return
    api = source.get_server().get_plugin_instance('minecraft_data_api')

    selected_slot = api.get_player_info(source.player, 'SelectedItemSlot')
    selected_slotinfo = [i for i in api.get_player_info(
        source.player, 'Inventory') if i['Slot'] == selected_slot]
    if not len(selected_slotinfo):
        selected_slotinfo = None

    head_slotinfo = [i for i in api.get_player_info(
        source.player, 'Inventory') if i['Slot'] == 103]
    if not len(head_slotinfo):
        head_slotinfo = None

    item1 = slot_item_decode(selected_slotinfo)
    item2 = slot_item_decode(head_slotinfo)

    slot1 = 'container.'+str(selected_slot)
    slot2 = 'armor.head'

    if item1['id'].endswith(('boots', 'leggings', 'chestplate', 'Elytra')):
        source.reply('§c其他部位的物品無法裝備到頭上')
        return
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
    server.register_help_message('!!hat', '把手上的物品戴到頭上')
    server.register_command(Literal('!!hat').runs(put_on))
