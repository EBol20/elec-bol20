from elec_bol20 import *
import elec_bol20.util as ebu
import bokeh.layouts
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import Figure, output_file, show
import bokeh.tile_providers
from bokeh.transform import linear_cmap
from bokeh.transform import log_cmap


# ###### abrir los datos
# abrimos los datos del padrón de votación del 2019

class CartoPlots:
    # DEFINICIONES
    MYE = -5
    MYS = -25
    MXE = -50
    MXS = -75
    CYE = -5
    CYS = -25
    CXE = -50
    CXS = -75
    BAR_TITLE = "CC  < diferencia [%] >  MAS"
    # PIXELS
    FIG_WIDTH = 700
    C_BAR_HIGH = 80
    C_BAR_LOW = -80
    PALETTE = ebu.P_DIF
    CART_SLIDER_INIT = .5
    FILE_OUT = ebu.DIR + '/htlml_1_intermedios/2020/'

    MAP_CIRCLE_SIZE_OFFSET = 5
    RATIO_CIRCLE_MAP = 7
    RATIO_CIRCLE_CARTO = 500
    BAR_TITLE_DIC = {
        "d_mas_cc": "CC < diferencia [%] > MAS",
        "diff": "CC < diferencia [%] > MAS",
        "cc": "CC [%]",
        "mas": "MAS-IPSP [%]",
        "creemos": "CREEMOS [%]",
        "fpv": "FPV [%]",
        "pan_bol": "PAN_BOL [%]"
    }
    TOOL_TIP_DIC = {
        "d_mas_cc": [
            ('Inscritos', '@HAB'),
            ('PAIS, Municipalidad', '@PAIS, @MUN'),
            ('Recinto', '@REC'),
            ('MAS [%]', '@mas{0.0}'),
            ('CC [%]', '@cc{0.0}'),
            ('Diferencia [%]', '@ad_mas_cc{0.0} (@mas_o_cc)'),
            ('------', '------')
            # ('DEN %', '@DEN')
            # ('PAIS', '@PAIS'),
        ],
        "diff": [
            ('Inscritos', '@HAB'),
            ('PAIS, Municipalidad', '@PAIS, @MUN'),
            ('Recinto', '@REC'),
            ('MAS [%]', '@mas{0.0}'),
            ('CC [%]', '@cc{0.0}'),
            ('Diferencia [%]', '@ad_mas_cc{0.0} (@mas_o_cc)'),
            ('------', '------')
            # ('DEN %', '@DEN')
            # ('PAIS', '@PAIS'),
        ],
        "cc": [
            ('Inscritos', '@HAB'),
            ('PAIS, Municipalidad', '@PAIS, @MUN'),
            ('Recinto', '@REC'),
            ('CC [%]', '@cc{0.0}'),
            ('------', '------')
        ],
        "mas": [
            ('Inscritos', '@HAB'),
            ('PAIS, Municipalidad', '@PAIS, @MUN'),
            ('Recinto', '@REC'),
            ('MAS [%]', '@mas{0.0}'),
            ('------', '------')
        ],
        "creemos": [
            ('Inscritos', '@HAB'),
            ('PAIS, Municipalidad', '@PAIS, @MUN'),
            ('Recinto', '@REC'),
            ('CREEMOS [%]', '@creemos{0.0}'),
            ('------', '------')
        ],
        "fpv": [
            ('Inscritos', '@HAB'),
            ('PAIS, Municipalidad', '@PAIS, @MUN'),
            ('Recinto', '@REC'),
            ('FPV [%]', '@fpv{0.0}'),
            ('------', '------')
        ],
        "pan_bol":
            [
                ('Inscritos', '@HAB'),
                ('PAIS, Municipalidad', '@PAIS, @MUN'),
                ('Recinto', '@REC'),
                ('PAN_BOL [%]', '@pan_bol{0.0}'),
                ('------', '------')
            ]

    }

    #
    # df = ebu.open_combine_2019()
    # needed_cols = ['X', 'Y', 'd_mas_cc', 'r', 'LAT', 'LON', 'PAIS', 'REC', 'MUN', 'DEN'
    #                                                                                   'GX', 'GY']
    def __init__(self):
        pass

    def load_file(self, df, _mean=['X', 'Y', 'LAT', 'LON', 'DEN', ],
                  _sum=['HAB', 'CC', 'MAS', 'PDC', 'VV'],
                  _first=['PAIS', 'REC', 'MUN', 'BOL']):
        # agrupamos por recinto
        _gr = df.groupby('ID_RECI')
        rec_df = _gr[_mean].mean()
        rec_df[_sum] = _gr[_sum].sum()
        rec_df[_first] = _gr[_first].first()

        rec_df['D_MAS_CC'] = rec_df['MAS'] - rec_df['CC']
        rec_df['d_mas_cc'] = rec_df['D_MAS_CC'] / rec_df['VV'] * 100
        rec_df['cc'] = rec_df['CC'] / rec_df['VV'] * 100
        rec_df['mas'] = rec_df['MAS'] / rec_df['VV'] * 100
        rec_df['creemos'] = rec_df['CREEMOS'] / rec_df['VV'] * 100
        rec_df['fpv'] = rec_df['FPV'] / rec_df['VV'] * 100
        rec_df['pan_bol'] = rec_df['PAN_BOL'] / rec_df['VV'] * 100

        rec_df['r'] = np.sqrt(rec_df['HAB']) / self.RATIO_CIRCLE_CARTO
        rec_df['r2'] = np.sqrt(
            rec_df['HAB']) / self.RATIO_CIRCLE_MAP + self.MAP_CIRCLE_SIZE_OFFSET

        res = ebu.lola_to_cart(rec_df['LON'].values, rec_df['LAT'].values)
        rec_df['GX'] = res[0]
        rec_df['GY'] = res[1]

        rec_df = rec_df.sort_values('DEN', axis=0, ascending=True)

        # remove nans
        rec_df = rec_df.dropna(axis=0)
        assert rec_df.isna().sum().sum() == 0
        return rec_df

    def plot_carto_single(self, data, frente, palette, path=FILE_OUT,
                          name_file="", low=0, high=100, show_plot=True):
        """

        :param data: df loaded by data_load
        :param frente: string, name of "partido" lowercase: diff, mas, cc, creemos, fpv, pan_bol
        :param palette: ej: P_GRAD_CC
        :param name_file: default:test
        :param low: cmap low limit: default: -80
        :param high: cmap high limit: defauilt: +80.
        :return: df
        """
        if frente == "diff":
            low = self.C_BAR_LOW
            high = self.C_BAR_HIGH
            frente = "d_mas_cc"

        bokeh.plotting.output_file(
            path + 'z037_' + frente + '_' + name_file + '.html')
        bokeh.plotting.output_file(
            os.path.join(
                os.path.dirname(ebu.DIR), 'docs',
                'graficas_htmls',
                'z037_' + frente + '_' + 'latest' + '.html'
            ))

        cart_init_val = self.CART_SLIDER_INIT  # add slider
        data['x'] = data['LON'] * (1 - cart_init_val) + data[
            'X'] * cart_init_val
        data['y'] = data['LAT'] * (1 - cart_init_val) + data[
            'Y'] * cart_init_val
        cm = linear_cmap(frente, palette=palette, low=low, high=high)

        data['mas'] = data['MAS'] / data['VV'] * 100
        data['cc'] = data['CC'] / data['VV'] * 100
        data['creemos'] = data['CREEMOS'] / data['VV'] * 100
        data['fpv'] = data['FPV'] / data['VV'] * 100
        data['pan_bol'] = data['PAN_BOL'] / data['VV'] * 100
        data['ad_mas_cc'] = data['d_mas_cc'].abs()
        data['mas_o_cc'] = 'n'
        data.loc[data['d_mas_cc'] >= 0, 'mas_o_cc'] = 'MAS'
        data.loc[data['d_mas_cc'] < 0, 'mas_o_cc'] = 'CC'

        source_master = ColumnDataSource(data)
        source_red_map = ColumnDataSource({'gx': [], 'gy': []})
        la, lo = ebu.get_la_lo_bolivia()
        source_bol = ColumnDataSource({'la': la, 'lo': lo})
        # source_red_car = ColumnDataSource({'lo': [], 'la': []})

        # JS CODE
        code_draw_red_map = """
        const data = {'gx': [], 'gy': []}
        const indices = cb_data.index.indices
        for (var i = 0; i < indices.length; i++ ) {
                data['gx'].push(source_master.data.GX[indices[i]])
                data['gy'].push(source_master.data.GY[indices[i]])
        }
        source_red_map.data = data
        """

        code_draw_red_car = """
        const data = {'lo': [], 'la': []}
        const indices = cb_data.index.indices
        for (var i = 0; i < indices.length; i++) {
                data['lo'].push(source_master.data.x[indices[i]])
                data['la'].push(source_master.data.y[indices[i]])
        }
        source_red_car.data = data
        """

        code_merged = """
        const data_map = {'lo': [], 'la': []}
        const data_car = {'gx': [], 'gy': []}
        const indices = cb_data.index.indices
        for (var i = 0; i < indices.length; i++) {
                data_map['lo'].push(source_master.data.x[indices[i]])
                data_map['la'].push(source_master.data.y[indices[i]])
                data_car['gx'].push(source_master.data.GX[indices[i]])
                data_car['gy'].push(source_master.data.GY[indices[i]])
        }
        source_red_car.data = data_car
        source_red_map.data = data_map
        """

        code_slider = """
            var data = source.data;
            var f = cb_obj.value
            var x = data['x']
            var y = data['y']
            var Y = data['Y']
            var X = data['X']
            var lat = data['LAT']
            var lon = data['LON']
            for (var i = 0; i < x.length; i++) {
                y[i] = (1-f)*lat[i] + f*Y[i]
                x[i] = (1-f)*lon[i] + f*X[i]
            }
            source.change.emit();
        """

        # FIGURES
        curr_time = ebu.get_bolivian_time(-3)
        # from datetime import datetime
        # curr_time = datetime.utcnow()

        pw = self.FIG_WIDTH
        cart_fig = Figure(plot_width=pw, plot_height=pw, output_backend="webgl",

                          )
        map_fig = Figure(plot_width=pw, plot_height=pw,
                         x_axis_type='mercator',
                         y_axis_type='mercator',
                         output_backend="webgl",
                         title="Última actualización: " + curr_time[
                             "datetime_val"].strftime(
                             "%Y-%m-%d %H:%M") + "BOT",
                         )
        cart_fig.background_fill_color = "grey"
        cart_fig.background_fill_alpha = .5
        # cb_fig = bokeh.plotting.Figure(plot_height=pw,plot_width=)
        # cb_fig.toolbar.logo = None
        # cb_fig.toolbar_location = None

        # SCATTER
        # noinspection PyUnresolvedReferences
        # add tiles
        tile_provider = bokeh.tile_providers.get_provider(
            bokeh.tile_providers.Vendors.CARTODBPOSITRON)
        map_fig.add_tile(tile_provider)

        # scatter in map
        map_fig.scatter(
            'GX', 'GY', source=source_master, size='r2',
            color=cm
        )

        # todo if we wont use map then we nee to delete the source
        # cart_fig.line('lo', 'la', source=source_bol, color='black')
        cart_fig.scatter('x', 'y', source=source_master, radius='r',
                         color=cm
                         )

        red_scat_map = map_fig.circle_cross('gx', 'gy',
                                            source=source_red_map,
                                            #                                color='red',
                                            fill_color=None,
                                            #                                line_color='green',
                                            size=20,
                                            line_color="white",
                                            line_width=4
                                            )

        red_scat_map = map_fig.circle_cross('gx', 'gy',
                                            source=source_red_map,
                                            #                                color='red',
                                            fill_color=None,
                                            #                                line_color='green',
                                            size=20,
                                            line_color="red",
                                            line_width=1
                                            )
        # red_scat_car = cart_fig.scatter('lo', 'la',
        # source=source_red_car, color='green')

        # add a hover tool that sets the link data for a hovered circle

        # callbacks
        callback_red_map = CustomJS(
            args={'source_master': source_master,
                  'source_red_map': source_red_map,
                  # 'source_red_car':source_red_car
                  },
            code=code_draw_red_map)
        # code = code_merged)

        # callback_red_car = CustomJS(
        #     args={'source_master': source_master, 'source_red_car': source_red_car},
        #     code=code_draw_red_car)

        # tools

        hover_cart = bokeh.models.HoverTool(
            tooltips=self.TOOL_TIP_DIC[frente],
            callback=callback_red_map,
            # renderers = [red_scat_car]

        )
        cart_fig.add_tools(hover_cart, )

        hover_map = bokeh.models.HoverTool(
            tooltips=self.TOOL_TIP_DIC[frente],
            # callback=callback_red_car,
            # renderers = [red_scat_map]
        )
        map_fig.add_tools(hover_map, )

        # slider
        callback_slider = CustomJS(args=dict(source=source_master),
                                   code=code_slider)

        slider = Slider(start=0, end=1, value=cart_init_val, step=.02,
                        title="carto")
        slider.js_on_change('value', callback_slider)

        # COLOR BAR
        ml = {int(i): str(np.abs(i)) for i in np.arange(-80, 81, 20)}
        cb = bokeh.models.ColorBar(
            color_mapper=cm['transform'],
            width=int(.9 * self.FIG_WIDTH),
            location=(0, 0),
            #     title="DEN (N/km^2)",
            # title=(BAR_TITLE),
            # margin=0,padding=0,
            title_standoff=10,
            # ticker=bokeh.models.LogTicker(),
            orientation='horizontal',
            major_label_overrides=ml

        )

        cart_fig.add_layout(cb, 'above')
        # cb.title_text_align = 'left'
        cart_fig.title.text = self.BAR_TITLE_DIC[frente]
        cart_fig.title.align = 'center'

        # layout = row(column(slider, cart_f),map_f)
        layout = bokeh.layouts.gridplot(
            [[slider, None], [cart_fig, map_fig]], sizing_mode='scale_width',
            merge_tools=False)
        layout.max_width = 1400
        # layout = bokeh.layouts.column([slider, cart_fig])

        cart_fig.x_range.start = self.CXS
        cart_fig.x_range.end = self.CXE
        cart_fig.y_range.start = self.CYS
        cart_fig.y_range.end = self.CYE

        _ll = ebu.lola_to_cart(lo=[self.MXS, self.MXE], la=[self.MYS, self.MYE])
        map_fig.x_range.start = _ll[0][0]
        map_fig.x_range.end = _ll[0][1]
        map_fig.y_range.start = _ll[1][0]
        map_fig.y_range.end = _ll[1][1]

        cart_fig.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        cart_fig.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        cart_fig.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        cart_fig.yaxis.minor_tick_line_color = None
        cart_fig.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
        cart_fig.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
        if show_plot:
            bokeh.plotting.show(layout)

        return data

# def download_file(url):
#     local_filename = url.split('/')[-1]
#     r = requests.get(url, stream=True)
#     with open(local_filename, 'wb') as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             if chunk:
#                 f.write(chunk)
#     return local_filename
#
# wd.get('https://www.dnb.no/bedrift/markets/analyser/arkiv/anbefalteaksjer.html')
# time.sleep(5)
#
# pdfLinks = wd.find_elements_by_css_selector('.moduleItemPdf > a')
#
# for linkElement in pdfLinks:
#     filename=download_file(linkElement.get_attribute("href"))
#     print(filename)
#
#
#
# time.sleep(5)
# wd.quit()