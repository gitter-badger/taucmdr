/**
 * FrontpageController
 *
 * @description :: Server-side logic for managing views
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

module.exports = {

  /**
   * Render the frontpage
   *
   * @param {Object} req
   * @param {Object} res
   */
  main: function (req, res) {
    res.view('frontpage/main');
  }
	
};

