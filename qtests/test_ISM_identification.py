import pytest
import sys
import sqlite3
sys.path.append("..")
import talonQ as talon
from helper_fns import *
@pytest.mark.integration

class TestIdentifyISM(object):

    def test_ISM_suffix(self):
        """ Example where the transcript is an ISM with suffix
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build, "TALON")        
        transcript_dict = talon.make_transcript_dict(cursor)

        edge_IDs = (3, 4, 5)
        vertex_IDs = (3, 4, 5, 6)
        v_novelty = (0, 0, 0, 0)

        gene_ID, transcript_ID, novelty = talon.process_ISM(edge_IDs, vertex_IDs,
                                                      transcript_dict,
                                                      run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor) 
        assert gene_ID == correct_gene_ID
        #assert novelty == [('TALON-5', 'ISM', '1'), ('TALON-5', 'ISM_suffix', '1')]
        conn.close()

    def test_ISM_prefix(self):
        """ Example where the transcript is a prefix ISM with a novel start
        """
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build, "TALON")
        transcript_dict = talon.make_transcript_dict(cursor)

        edge_IDs = (200,2,3)
        vertex_IDs = (500, 2, 3, 4) 
        v_novelty = (1, 0, 0, 0)
        gene_ID, transcript_ID, novelty = talon.process_ISM(edge_IDs, vertex_IDs,
                                                            transcript_dict,
                                                            run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor)
        assert gene_ID == correct_gene_ID
        #assert novelty == [('TALON-5', 'ISM', '1'), 
        #                   ('TALON-5', 'ISM_prefix', '1'), 
        #                   ('TALON-5', '5p', None)]
   
        conn.close()

    def test_monoexonic_ISM(self):
        """ Monoexonic ISM """
        
        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build, "TALON")
        transcript_dict = talon.make_transcript_dict(cursor)

        edge_IDs = (5,)
        vertex_IDs = (5, 6)
        v_novelty = (0, 0)

        gene_ID, transcript_ID, novelty = talon.process_ISM(edge_IDs, vertex_IDs,
                                                            transcript_dict,
                                                            run_info)

        correct_gene_ID = fetch_correct_ID("TG1", "gene", cursor)
        assert gene_ID == correct_gene_ID
        #assert novelty == [('TALON-5', 'ISM', '1'), ('TALON-5', 'ISM_suffix', '1')]
        conn.close()

    def test_no_match(self):
        """ Example with no ISM match """

        conn, cursor = get_db_cursor()
        build = "toy_build"
        edge_dict = talon.make_edge_dict(cursor)
        location_dict = talon.make_location_dict(build, cursor)
        run_info = talon.init_run_info(cursor, build, "TALON")
        transcript_dict = talon.make_transcript_dict(cursor)

        edge_IDs = (1, 2, 3, 100, 200) 
        vertex_IDs = (1, 2, 3, 4, 50, 70) 
        v_novelty = (0, 0, 0, 0, 1, 1)

        gene_ID, transcript_ID, novelty = talon.process_ISM(edge_IDs, vertex_IDs,
                                                            transcript_dict,
                                                            run_info)
        assert gene_ID == transcript_ID == novelty == None 
        conn.close()       
