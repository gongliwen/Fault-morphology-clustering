import matplotlib.pyplot as pltimport numpy as np# import obspy# import matplotlib.patheffects as PathEffectsfrom mpl_toolkits.basemap import Basemapimport sysfrom load_fault_traces import load_fault_tracesimport Load_Dataimport pickle class empty:    passdb = pickle.load(open('../stored_variables/'+'dbresults','rb'))## Don't delete these commented lines. May need them again later. # Dictionary with Boolean arrays to keep track of cluster-fault name relationshp. This is only preliminary! If the cluster labels have changed, the script should be able to keep track of that. # Can either create hypo_faults now if the db results are pretty good, then manually determine the label number to fault name relationship, and save the file, # or load the previously determined hypo_faults variable. # hypo_faults = {'Paganica'      :db.labels==0,#                'Campotosto'    :db.labels==1,#                'Cittareale'    :db.labels==7,#                'Mt. San Franco':db.labels==3,#                'Noise'         :db.labels==-1}# pickle.dump(hypo_faults, open('../stored_variables/preliminary_clusters','wb'))hypo_faults = pickle.load(open('../stored_variables/preliminary_clusters','rb'))# Keep track of ALL colors while will be used and added to the legend (fault traces and aftershocks)fault_color_dict = {                    'Paganica':'#32a852',                      'Campotosto':'#4f4fff',                     'Cittareale':'#c74c00',                    'Mt. San Franco':'#ff8c00',                    # bellow address faults which are only present in fault traces                    'Mt. Stabiata':'#a900c7',                    'Mt. Castellano-Colle Enzano':'#f2ff00',                    'San Demetrio':'#ff0000',                    #                    'Surface rupture':'#ff0000',                    'Noise'     :'#E6E6E6',                    }#'#757575'}# Convert from names in the fault trace file to names I want in the legend. trace_to_label = {'M.Stabbiata':'Stabiata',                  'M.S.Franco':'Mt. San Franco',                  'Aternosys.2':'Paganica',                  'Aternosys.6':'Paganica',                  'Aternosys.7':'Paganica',                  'Aternosys.8':'Paganica',                  'Campotosto':'Campotosto',                  'Cittareale':'Cittareale',                  'Mt.Castellano':'Castellano-Colle Enzano',                  'C.lleEnzano':'Castellano-Colle Enzano',                  'SanDemetrio':'San Demetrio',                  'D.Demetrio':'San Demetrio'                  }    def get_cluster_color(labels, label, hypo_faults, fault_color_dict):    similarity = np.zeros(len(hypo_faults)) # similarity between currently observed cluster and each previously named cluster.     name = np.zeros(len(hypo_faults), dtype = object)    for ikey, key in enumerate(hypo_faults.keys()):        similarity[ikey] = (hypo_faults[key] * (labels == label)).sum()/(hypo_faults[key].sum()) # Similarity is basically normalized zero lag cross correlation between the boolean aray of this cluster and each previously named cluster        if similarity[ikey] <= 0:            name[ikey] = None        elif similarity[ikey] > 0:            name[ikey] = key    if (similarity>0).any():        fault_name = name[similarity == similarity.max()][0]     else:        fault_name = 'not present'    color_db    = fault_color_dict.get(fault_name, None)    return fault_name, color_dbplt.rcParams.update({'font.size': 16})if True:     width = 80000 # 2000000    height = 80000 # 2000000    centlat = 42.4    centlon = 13.4        fig, ax = plt.subplots(figsize = (10, 10))        map = Basemap(projection='aeqd',              lon_0 = centlon,              lat_0 = centlat,              width = width,              height = height,              resolution = 'i',                  ax = ax)        # map.drawmapboundary(fill_color=None)    # map.fillcontinents(color='lightgrey',lake_color=None)    # map.shadedrelief()    # map.etopo(scale = 1)    # map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)    # map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)    x, y = map(db.lon, db.lat)        # Plot clusters    # Pain in the ass script to decide which fault is which. Look for the clusters which are most similar to previously named clusters.     zorder_dict = {'Noise':.11, 'Campotosto':.12, 'Mt. San Franco':.13, 'Paganica':.14} # Need to know which clusters to plot first, to determine which points are covered by other points.     # point_labels = np.zeros(len(db.labels), dtype = object)    # point_colors = np.zeros(db.labels.shape, dtype = object)    for ilabel, label in enumerate(np.unique(db.labels)):        fault_name, color_db = get_cluster_color(db.labels, label, hypo_faults, fault_color_dict)        this = db.labels == label        # point_colors[this] = color_db         plt.scatter(x[this], y[this], #label = fault_name,                    s = 1, color = color_db,                     zorder = zorder_dict.get(fault_name, 100))#, linewidths = .2,                 # Plot surface ruptures    mf, sr = load_fault_traces()      for ifault, fault in enumerate(sr):        x, y = map(fault['lons'], fault['lats'])        plt.plot(x, y, c = 'r', linewidth = 5, zorder = 10)            # Plot mapped faults.     for ifault, fault in enumerate(mf):        x, y = map(fault['lons'], fault['lats'])        # print(fault['name'])        fault_name = trace_to_label.get(fault['name'],'not present')        plt.plot(x, y, color = fault_color_dict.get(fault_name, '#000000'), zorder = 10.1)                x, y = map(fault['lonlabel'], fault['latlabel'])        plt.annotate(fault['name'], [x,y] , size = 5)    # Make a legend: only really concerned about portraying colors, so do a trick that makes a dot legend entry for each color used.     markers = [plt.Line2D([-2000000,0],[-200000,0],color=color, marker='o', linestyle='') for color in fault_color_dict.values()]    plt.legend(markers, fault_color_dict.keys(), numpoints=1)            # xax = ax.get_xaxis()        # map.drawmapscale(-86, 28, -81, 35.5, 250, fontsize = 12)    plt.show()        # plt.savefig('/Users/brennanbrunsvik/Documents/UCSB/ENAM/Writing_2020/Research_proposal/stations_raw.png', dpi = 250)