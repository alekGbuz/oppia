// Copyright 2013 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


// This is needed in order to register the directive in the
// GENERATOR_ID_TO_DIRECTIVE_MAPPING in valueGeneratorEditor.js.
GENERATOR_ID_TO_DIRECTIVE_MAPPING['RangeRestrictedCopier'] = 'range-restricted-copier';

oppia.directive('rangeRestrictedCopier', function($compile, warningsData) {
  return {
    link: function(scope, element, attrs) {
      scope.getTemplateUrl = function() {
        return VALUE_GENERATOR_TEMPLATES_URL + scope.generatorId;
      };
      $compile(element.contents())(scope);
    },
    restrict: 'E',
    scope: true,
    template: '<div ng-include="getTemplateUrl()"></div>',
    controller: function($scope, $attrs) {
      $scope.generatorId = $scope.$parent.generatorId;
      $scope.initArgs = $scope.$parent.initArgs;
      $scope.customizationArgs = $scope.$parent.customizationArgs;
      $scope.objType = $scope.$parent.objType;

      $scope.$watch($scope.customizationArgs, function(newValue, oldValue) {
        // TODO(sll): This does not have any effect; why?
        if (newValue !== undefined || oldValue !== undefined) {
          if (newValue > $scope.initArgs.upper_bound || newValue < $scope.initArgs.lower_bound) {
            warningsData.addWarning(
              'Value must be between ' + $scope.initArgs.upper_bound +
              ' and ' + $scope.initArgs.lower_bound + ', inclusive.');
            return;
          }
        }
      });
    }
  };
});
