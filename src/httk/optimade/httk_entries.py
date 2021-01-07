#!/usr/bin/env python
#
#    The high-throughput toolkit (httk)
#    Copyright (C) 2012-2020 Rickard Armiento
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from httk.optimade import optimade_entries

httk_all_entries = ['structures','calculations']
httk_entry_info = {
  'structures': {
      'description': optimade_entries.entry_info['structures']['descripion'],
      'properties': {
          'id': optimade_entries.entry_info['structures']['properties']['id'],
          'type': optimade_entries.entry_info['structures']['properties']['type'],
          'elements': optimade_entries.entry_info['structures']['properties']['elements'],
          'nelements': optimade_entries.entry_info['structures']['properties']['nelements'],
          'chemical_formula_descriptive': optimade_entries.entry_info['structures']['properties']['chemical_formula_descriptive'],
          'dimension_types': optimade_entries.entry_info['structures']['properties']['dimension_types'],
          'nperiodic_dimensions': optimade_entries.entry_info['structures']['properties']['nperiodic_dimensions'],
          'lattice_vectors': optimade_entries.entry_info['structures']['properties']['lattice_vectors'],
          'structure_features': optimade_entries.entry_info['structures']['properties']['structure_features'],
      }
  },
  'calculations': {
      'description': optimade_entries.entry_info['calculations']['descripion'],
      'properties': {
          'id': optimade_entries.entry_info['calculations']['properties']['id'],
          'type': optimade_entries.entry_info['calculations']['properties']['type'],
      }
  },
  #'references': {
  #    'descripion': optimade_entries.entry_info['references']['descripion'],
  #    'properties': {
  #        'id': optimade_entries.entry_info['references']['properties']['id'],
  #        'type': optimade_entries.entry_info['references']['properties']['type'],
  #    }
  #},
}

httk_entry_info['structures']['properties']['structure_features']['default_response']=True
httk_entry_info['structures']['properties']['lattice_vectors']['default_response']=True
httk_entry_info['structures']['properties']['elements']['default_response']=True
httk_entry_info['structures']['properties']['nelements']['default_response']=True
httk_entry_info['structures']['properties']['chemical_formula_descriptive']['default_response']=True
httk_entry_info['structures']['properties']['dimension_types']['default_response']=True
httk_entry_info['structures']['properties']['nperiodic_dimensions']['default_response']=True

#dict([(x,optimade_entries.entry_info[x]) for x in optimade_entries.entry_info if x in httk_all_entries])
httk_valid_endpoints = list(['info', 'versions', 'links'] + httk_all_entries + ["info/"+x for x in httk_all_entries] + [''])
httk_properties_by_entry = dict([(x, httk_entry_info[x]['properties'].keys()) for x in httk_entry_info])
httk_valid_response_fields =  httk_properties_by_entry

default_response_fields = {}

# Set everyting to not be sortable
for entry in httk_all_entries:
    entry_default_response_fields = []
    for p in httk_entry_info[entry]['properties']:
        httk_entry_info[entry]['properties'][p]['sortable'] = False
        if httk_entry_info[entry]['properties'][p]['default_response']:
            entry_default_response_fields += [p]
    default_response_fields[entry] =  entry_default_response_fields