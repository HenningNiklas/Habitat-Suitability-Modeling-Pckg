from .fun import *

def labler(thresholds,hsi):
    """"
    Creates a label for hsi values which can later be used in graphing to assign different colors to plot points
    :param thresholds list of hsi thresholds which mark the end of the bin
    :hsi

    """
    color_labels = np.empty(len(hsi))
    for thresh_index in range(len(thresholds[:-1])):
        for i in range(len(hsi)):
            if hsi[i] >= thresholds[thresh_index]:
                color_labels[i] = thresh_index+2
    return color_labels

def fr_to_hsi(fr_list,hsi_bins,fr_thresholds):
    """
        Converts forage ratio confidence intervals to hsi values using linear least squares regression
            :param fr_list: list of forage ratios per bin
            :param hsi_bins: list of hsi bin values with equal step size ex.[0,0.01,0.02 .... 0.99,1.00]
            :param fr_thresholds: list of forage ration confidence interval [upper_fr,lower_fr]
            :return hsi_fr_thresholds: list of converted hsi values from  [hsi_fr_lower,hsi_fr_upper]
            """
    fr = np.array(fr_list,dtype="f8")
    hsi = np.array(hsi_bins,dtype="f8")
    y_est = np.polyfit(hsi, fr, 2)
    if hsi_bins[0] == 0:
        bin_stepsize = hsi[1]
    else:
        bin_stepsize = hsi[0]

    hsi_fr_upper = round(round(np.interp(fr_thresholds[0], np.polyval(y_est, hsi), hsi)*(1/bin_stepsize))*bin_stepsize, 2)
    hsi_fr_lower = round(round(np.interp(fr_thresholds[1], np.polyval(y_est, hsi), hsi)*(1/bin_stepsize))*bin_stepsize, 2) #second round is to combat potential floating binary error
    hsi_fr_thresholds = [hsi_fr_lower, hsi_fr_upper]
    print("Fr lower and upper 95% conf interval", hsi_fr_lower, hsi_fr_upper)
    return hsi_fr_thresholds

# def algomerative_clustering_5bins(hsi_fr_thresholds,fr_list,hsi_bins):
#     """
#     Turn three bins into 5 using alogmerative clustering to seperate prefered and avoided bins
#         :param fr_list: list of forage ratios per bin
#         :param hsi_bins: list of hsi bin values with equal step size ex.[0,0.01,0.02 .... 0.99,1.00]
#         :param hsi_fr_thresholds: list of converted hsi values from  [hsi_fr_lower,hsi_fr_upper]
#
#     """
#
# #TODO error generating binning results
#     i_fr_up = int(np.where(hsi_bins == round(hsi_fr_thresholds[0], 2))[0]) + 1
#     i_fr_low = int(np.where(hsi_bins == round(hsi_fr_thresholds[1], 2))[0])
#
#     # print(i_fr_low,i_fr_up)
#     fr_array_avoid = fr_list[:i_fr_low]
#     fr_array_neutral = fr_list[i_fr_low:i_fr_up]
#     fr_array_prefer = fr_list[i_fr_up:]
#     fr_dict_list = []
#     fr_dict_list.append({"fr_type": "avoided", "fr_array": fr_array_avoid, "hsi_array": hsi_bins[:i_fr_low],
#                          "clusters": 2, "min_index": 0, "max_index": i_fr_low})
#     fr_dict_list.append({"fr_type": "prefered", "fr_array": fr_array_prefer, "hsi_array": hsi_bins[i_fr_up:],
#                          "clusters": 2, "min_index": i_fr_up, "max_index": -1})
#
#     thrsh = []
#     for dict in fr_dict_list:
#         print("Seperating",dict["fr_type"], "bin into two bins")
#         y = dict["fr_array"]
#         x = dict["hsi_array"]
#         data = list(zip(y, x))
#
#         c = np.arange(len(data)).reshape((-1, 1))
#         connect = kneighbors_graph(c, 2, mode='connectivity', include_self=True)
#         hierarchical_cluster = AgglomerativeClustering(n_clusters=dict["clusters"], affinity='euclidean',
#                                                        connectivity=connect, linkage='ward')
#         labels = hierarchical_cluster.fit_predict(data)
#
#         index = [dict["min_index"]]
#         index.append(np.where(labels[:-1] != labels[1:])[0][0] + dict["min_index"] + 1)
#         index.append(dict["max_index"])
#
#         for i in index:
#             thrsh.append(hsi_bins[i])
#     print(thrsh)
#     return thrsh

